function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('show');
}

// Close sidebar when clicking outside on mobile
document.addEventListener('click', function(event) {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    
    if (window.innerWidth <= 768) {
        if (!sidebar.contains(event.target) && !sidebarToggle.contains(event.target)) {
            sidebar.classList.remove('show');
        }
    }
});

// Handle window resize
window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        document.getElementById('sidebar').classList.remove('show');
    }
});

// Navigation history management for back button behavior
document.addEventListener('DOMContentLoaded', function() {
    
    // Utility function to set up navigation history
    function setupNavigationHistory(labCode) {
        console.log(`Setting up navigation history for lab: ${labCode}`);
        
        // Clear any existing history first
        while (window.history.length > 1) {
            window.history.back();
        }
        
        // Set up the navigation flow
        window.history.replaceState({
            page: 'labspace_dashboard',
            labCode: labCode,
            fromBase: true
        }, '', `/labspaces/lab/${labCode}/`);
        
        window.history.pushState({
            page: 'base_labspaces',
            fromDashboard: true
        }, '', '/labspaces/');
        
        console.log('Navigation history set up successfully');
        console.log('Current history state:', window.history.state);
    }
    
    // Check if we're on a labspace dashboard page
    const currentPath = window.location.pathname;
    const labspaceMatch = currentPath.match(/^\/labspaces\/lab\/([A-Z0-9]+)\/?$/);
    
    if (labspaceMatch) {
        // We're on a labspace dashboard page
        const labCode = labspaceMatch[1];
        
        // Check if we need to set up the navigation history
        if (window.history.state === null || !window.history.state.page) {
            setupNavigationHistory(labCode);
        }
    }
    
    // Handle back button navigation
    window.addEventListener('popstate', function(event) {
        console.log('Popstate event triggered:', event.state);
        
        if (event.state) {
            if (event.state.page === 'labspace_dashboard') {
                // User pressed back from base URL, redirect to dashboard
                const labCode = event.state.labCode;
                console.log(`Redirecting to dashboard for lab: ${labCode}`);
                if (labCode) {
                    window.location.href = `/labspaces/lab/${labCode}/`;
                }
            } else if (event.state.page === 'base_labspaces') {
                // User pressed back from dashboard, redirect to base URL
                console.log('Redirecting to base labspaces URL');
                window.location.href = '/labspaces/';
            }
        } else {
            // No state, likely navigating to a completely different page
            console.log('No state found, likely external navigation');
        }
    });
    
    // Handle direct navigation to dashboard (e.g., clicking dashboard link)
    const dashboardLinks = document.querySelectorAll('a[href*="/lab/"]');
    dashboardLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            const labCodeMatch = href.match(/\/lab\/([A-Z0-9]+)\/?$/);
            
            if (labCodeMatch) {
                const labCode = labCodeMatch[1];
                setupNavigationHistory(labCode);
            }
        });
    });
    
    // Handle navigation to base labspaces URL
    const baseLinks = document.querySelectorAll('a[href="/labspaces/"], a[href="/labspaces"]');
    baseLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Clear any existing labspace-specific history
            if (window.history.state && window.history.state.page === 'labspace_dashboard') {
                window.history.back();
            }
        });
    });
});