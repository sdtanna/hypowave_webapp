document.addEventListener('DOMContentLoaded', () => {
    // Example of setting the visitor total dynamically
    document.getElementById('visitorTotal').textContent = '';
    document.getElementById('stat2').textContent = '';
    document.getElementById('stat3').textContent = '';
    }
);

document.getElementById('currentBtn').addEventListener('click', function() {
    changeVisibility('visible', 'hidden');
    updateHeaderText("Current Occupancy");

    // Clear heatmap
    if (window.heatmapInstance) {
        window.heatmapInstance.setData({
            max: 0,
            data: []
        });
    }
});

document.getElementById('todayBtn').addEventListener('click', function() {
    changeVisibility('hidden', 'visible');
    updateHeaderText("Today's Occupancy");
    if (window.heatmapInstance) {
        window.heatmapInstance.setData({
            max: 0,
            data: []
        });
    }
});

document.getElementById('pastWeekBtn').addEventListener('click', function() {
    changeVisibility('hidden', 'visible');
    updateHeaderText("Past Week's Occupancy");
    if (window.heatmapInstance) {
        window.heatmapInstance.setData({
            max: 0,
            data: []
        });
    }
});

document.getElementById('submitDates').addEventListener('click', function() {
    const startDate = document.getElementById("startDate").value;
    const endDate = document.getElementById("endDate").value;
        
    if (startDate && endDate) {
        console.log(`Fetching data from ${startDate} to ${endDate}`);
        // Close modal if both dates selected
        document.getElementById("dates_modal").style.display = 'none';

        changeVisibility('hidden', 'visible');
        updateHeaderText(`Occupancy from ${startDate} to ${endDate}`);
        if (window.heatmapInstance) {
            window.heatmapInstance.setData({
                max: 0,
                data: []
            });
        }

    } else {
        alert('Please select both a start and end date.');
    }
});

function changeVisibility(element1Visibility, element2Visibility) {
    document.getElementById('plotDiv').classList.toggle('hidden', element1Visibility === 'hidden');
    document.getElementById('heatmap').classList.toggle('hidden', element2Visibility === 'hidden');

    // Save display status
    sessionStorage.setItem('element1Visibility', element1Visibility);
    sessionStorage.setItem('element2Visibility', element2Visibility);
}

function updateHeaderText(text) {
    document.getElementById("plot_header").textContent = text;
    sessionStorage.setItem('headerText', text);
}

// Apply stored states when page loads
window.onload = function() {
    var element1State = sessionStorage.getItem('element1Visibility');
    var element2State = sessionStorage.getItem('element2Visibility');
    var headerText = sessionStorage.getItem('headerText');

    // Update visibility
    if (element1State !== null && element2State !== null) {
        document.getElementById('plotDiv').classList.toggle('hidden', element1State === 'hidden');
        document.getElementById('heatmap').classList.toggle('hidden', element2State === 'hidden');
    } else {
        // Default state when opening in new session
        document.getElementById('plotDiv').classList.remove('hidden');
        document.getElementById('heatmap').classList.add('hidden');
    }

    // Update header text
    if (headerText !== null) {
        document.getElementById("plot_header").textContent = headerText;
    } else {
        // Default header text
        document.getElementById("plot_header").textContent = "Current Occupancy";
    }
};
  
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

function viewsettingsmodal() {
    var modal = document.getElementById("settings_modal");
    var close = document.getElementById("close_settings_btn");
  
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
  