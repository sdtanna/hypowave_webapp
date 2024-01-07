document.addEventListener('DOMContentLoaded', () => {
    // Example of setting the visitor total dynamically
    document.getElementById('visitorTotal').textContent = '120';
    document.getElementById('stat2').textContent = '250';
    document.getElementById('stat3').textContent = '350';
    }
);
  
document.addEventListener('DOMContentLoaded', () => {
    
    // Event listener for the Submit button within the date picker
    document.getElementById("submitDates").addEventListener('click', () => {
    const startDate = document.getElementById("startDate").value;
    const endDate = document.getElementById("endDate").value;
        
    if (startDate && endDate) {
        console.log(`Fetching data from ${startDate} to ${endDate}`);
        // Close modal if both dates selected
        document.getElementById("dates_modal").style.display = 'none';
    } else {
        alert('Please select both a start and end date.');
    }
    });
    
    // Adjusting headers on RHS
    document.getElementById("liveBtn").addEventListener('click', () => {
        document.getElementById("plot_header").textContent = "Live Occupancy"
    });
  
    document.getElementById("todayBtn").addEventListener('click', () => {
        document.getElementById("plot_header").textContent = "Today's Occupancy"
    });
  
    document.getElementById("pastWeekBtn").addEventListener('click', () => {
        document.getElementById("plot_header").textContent = "Past Week's Occupancy"
    });
  
    document.getElementById("submitDates").addEventListener('click', () => {
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;
          
        if (startDate && endDate) {
            document.getElementById("plot_header").textContent = `Occupancy from ${startDate} to ${endDate}` 
        }
    });
  
});
  
// Help Modal (About and Feedback Modals will be similar)
function viewhelpmodal() {
    var modal = document.getElementById("help_modal");
    var close = document.getElementById("close_help_btn");
  
    modal.style.display = "block";
  
    close.onclick = function() {
        modal.style.display = "none";
    }
  
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
};
  
// Date Selection Modal
function viewdatesmodal() {
    var modal = document.getElementById("dates_modal");
    var close = document.getElementById("close_dates_btn");
  
    modal.style.display = "block";
  
    close.onclick = function() {
        modal.style.display = "none";
        document.getElementById("startDate").value='0000-00-00';
        document.getElementById("endDate").value='0000-00-00';
    }
  
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
            document.getElementById("startDate").value='0000-00-00';
            document.getElementById("endDate").value='0000-00-00';
        }
    }
};
  