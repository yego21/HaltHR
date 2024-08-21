function setDateRange() {
    const dateRange = document.getElementById('date_range').value;
    const startDateField = document.getElementById('start_date');
    const endDateField = document.getElementById('end_date');

    let startDate = '';
    let endDate = new Date();

    if (dateRange === 'today') {
        startDate = new Date();
    } else if (dateRange === 'this_week') {
        startDate = new Date();
        startDate.setDate(endDate.getDate() - endDate.getDay()); // Start of the week (Sunday)
    } else if (dateRange === 'last_7_days') {
        startDate = new Date();
        startDate.setDate(endDate.getDate() - 6); // Last 15 days
    } else if (dateRange === 'last_15_days') {
        startDate = new Date();
        startDate.setDate(endDate.getDate() - 14); // Last 15 days          
    } else if (dateRange === 'last_30_days') {
        startDate = new Date();
        startDate.setDate(endDate.getDate() - 29); // Last 15 days
    }


    // Format the dates to 'YYYY-MM-DD' for the input fields
    const formatDate = (date) => date.toISOString().split('T')[0];

    if (startDate) {
        startDateField.value = formatDate(startDate);
    }
    endDateField.value = formatDate(endDate);
}
