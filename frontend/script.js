// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// Global state
let buildings = [];
let departments = [];
let tickets = [];
let currentUser = null;
let isLoggedIn = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    checkUserSession();
});

// Initialize application
function initializeApp() {
    // Setup sidebar toggle for mobile
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }
    
    // Setup sidebar navigation
    setupSidebarNavigation();
}

// Setup sidebar navigation
function setupSidebarNavigation() {
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    
    sidebarLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const section = link.getAttribute('data-section');
            showSection(section);
            
            // Update active state
            sidebarLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // Close sidebar on mobile
            const sidebar = document.getElementById('sidebar');
            if (window.innerWidth <= 1024) {
                sidebar.classList.remove('open');
            }
        });
    });
}

// Check user session
function checkUserSession() {
    const userId = localStorage.getItem('ict_user_id');
    const userName = localStorage.getItem('ict_user_name');
    
    if (userId && userName) {
        currentUser = {
            id: userId,
            name: userName
        };
        isLoggedIn = true;
        updateUserInterface();
        loadInitialData();
    } else {
        showLoginInterface();
    }
}

// Update user interface based on login status
function updateUserInterface() {
    const loginContainer = document.getElementById('login-container');
    const featuresGrid = document.getElementById('features-grid');
    const userProfile = document.getElementById('user-profile');
    const userIdSpan = document.getElementById('user-id');
    const userNameSpan = document.querySelector('.user-name');
    const loginStatus = document.getElementById('login-status');
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    
    if (isLoggedIn && currentUser) {
        // Hide login, show features
        if (loginContainer) loginContainer.style.display = 'none';
        if (featuresGrid) featuresGrid.style.display = 'grid';
        
        // Update user profile
        if (userNameSpan) userNameSpan.textContent = currentUser.name;
        if (userIdSpan) userIdSpan.textContent = currentUser.id;
        
        // Show logout button in profile
        if (logoutBtn) logoutBtn.style.display = 'block';
        
        // Update login status
        if (loginStatus) {
            loginStatus.innerHTML = `
                <div class="status-indicator online"></div>
                <span>Logged in as ${currentUser.name}</span>
            `;
        }
        
        // Update login button
        if (loginBtn) {
            loginBtn.innerHTML = `
                <i class="fas fa-sign-out-alt"></i>
                <span>Logout</span>
            `;
            loginBtn.onclick = handleLogout;
        }
        
        // Show dashboard by default
        showSection('dashboard');
    } else {
        // Show login, hide features
        if (loginContainer) loginContainer.style.display = 'block';
        if (featuresGrid) featuresGrid.style.display = 'none';
        
        // Reset user profile
        if (userNameSpan) userNameSpan.textContent = 'Guest User';
        if (userIdSpan) userIdSpan.textContent = 'Not logged in';
        
        // Hide logout button in profile
        if (logoutBtn) logoutBtn.style.display = 'none';
        
        // Reset login status
        if (loginStatus) {
            loginStatus.innerHTML = `
                <div class="status-indicator offline"></div>
                <span>Not logged in</span>
            `;
        }
        
        // Reset login button
        if (loginBtn) {
            loginBtn.innerHTML = `
                <i class="fas fa-sign-in-alt"></i>
                <span>Login to Continue</span>
            `;
            loginBtn.onclick = handleLogin;
        }
        
        // Show home page
        showSection('home');
    }
}

// Show login interface
function showLoginInterface() {
    showSection('home');
    updateUserInterface();
}

// Handle one-click login
async function handleLogin() {
    if (isLoggedIn) {
        handleLogout();
        return;
    }
    
    try {
        // Generate unique user ID
        const userId = generateUserId();
        const userName = `User_${userId.substring(0, 8)}`;
        
        // Create user session
        currentUser = {
            id: userId,
            name: userName
        };
        
        // Store in localStorage
        localStorage.setItem('ict_user_id', userId);
        localStorage.setItem('ict_user_name', userName);
        
        isLoggedIn = true;
        
        // Update UI
        updateUserInterface();
        
        // Show success notification
        showNotification('Successfully logged in!', 'success');
        
        // Load initial data
        await loadInitialData();
        
    } catch (error) {
        console.error('Login error:', error);
        showNotification('Login failed. Please try again.', 'error');
    }
}

// Handle logout
function handleLogout() {
    // Clear session
    localStorage.removeItem('ict_user_id');
    localStorage.removeItem('ict_user_name');
    
    currentUser = null;
    isLoggedIn = false;
    
    // Update UI
    updateUserInterface();
    
    // Show notification
    showNotification('Successfully logged out!', 'success');
}

// Invite teammate function
function inviteTeammate() {
    if (!isLoggedIn) {
        showNotification('Please login first to invite teammates.', 'error');
        return;
    }
    
    // For now, show a simple notification
    // In a real implementation, this would open a modal or redirect to admin panel
    showNotification('Team invitation feature coming soon! Contact your administrator for user management.', 'success');
}

// Update home page KPI cards
function updateHomeKPIs(data) {
    const totalTickets = document.getElementById('kpi-total-tickets');
    const activeAgents = document.getElementById('kpi-active-agents');
    const resolutionTime = document.getElementById('kpi-resolution-time');
    const aiStatus = document.getElementById('kpi-ai-status');
    
    if (totalTickets && data.total_tickets !== undefined) {
        totalTickets.querySelector('.kpi-value').textContent = data.total_tickets;
    }
    
    if (activeAgents) {
        // Set to 3 for now, could be fetched from backend
        activeAgents.querySelector('.kpi-value').textContent = '3';
    }
    
    if (resolutionTime && data.avg_resolution_time) {
        resolutionTime.querySelector('.kpi-value').textContent = data.avg_resolution_time;
    } else if (resolutionTime) {
        resolutionTime.querySelector('.kpi-value').textContent = '2.3h';
    }
    
    if (aiStatus) {
        // Always show AI as online
        const aiValue = aiStatus.querySelector('.kpi-value');
        aiValue.textContent = 'Online';
        aiValue.style.color = '#10b981';
    }
}

// Generate unique user ID
function generateUserId() {
    return 'user_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Setup event listeners
function setupEventListeners() {
    // Ticket form submission
    const ticketForm = document.getElementById('ticket-form');
    if (ticketForm) {
        ticketForm.addEventListener('submit', handleTicketSubmission);
    }

    // Chat input
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keypress', handleChatKeyPress);
    }
}

// Navigation functions
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });
    
    // Show selected section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
        
        // Update sidebar navigation
        document.querySelectorAll('.sidebar-link').forEach(link => {
            link.classList.remove('active');
        });
        
        const activeLink = document.querySelector(`[data-section="${sectionId}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }
        
        // Load data for specific sections
        if (sectionId === 'dashboard' && isLoggedIn) {
            loadDashboard();
        } else if (sectionId === 'tickets' && isLoggedIn) {
            loadTickets();
        }
    } else {
        console.error(`Section with id '${sectionId}' not found`);
        // Fallback to dashboard if section doesn't exist
        const dashboardSection = document.getElementById('dashboard');
        if (dashboardSection) {
            dashboardSection.classList.add('active');
            if (isLoggedIn) {
                loadDashboard();
            }
        }
    }
}

// API Functions
async function makeAPIRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
        },
        ...options
    };
    
    // Add user ID to requests if logged in
    if (currentUser && currentUser.id) {
        config.headers['X-User-ID'] = currentUser.id;
    }
    
    // Add timeout for AI requests to handle slow responses
    const isAIRequest = endpoint.includes('/ai/');
    if (isAIRequest) {
        config.signal = AbortSignal.timeout(15000); // 15 second timeout for AI requests
    }
    
    try {
        const response = await fetch(url, config);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Load initial data
async function loadInitialData() {
    if (!isLoggedIn) return;
    
    try {
        console.log('Loading initial data...');
        
        // Load buildings first
        await loadBuildings();
        
        // Load departments immediately (not just when building is selected)
        await loadAllDepartments();
        
        // Load other data
        await Promise.all([
            loadTickets(),
            loadDashboard()
        ]);
        
        console.log('Initial data loaded successfully');
    } catch (error) {
        console.error('Error loading initial data:', error);
        showNotification('Error loading data. Please refresh the page.', 'error');
    }
}

// Load buildings
async function loadBuildings() {
    try {
        console.log('Loading buildings...');
        const data = await makeAPIRequest('/buildings');
        buildings = data.buildings;
        console.log('Buildings loaded:', buildings);
        
        // Populate building dropdowns
        const buildingSelects = document.querySelectorAll('#building, #building-filter');
        console.log('Found building selects:', buildingSelects.length);
        
        buildingSelects.forEach(select => {
            select.innerHTML = '<option value="">Select Building</option>';
            buildings.forEach(building => {
                const option = document.createElement('option');
                option.value = building.name;
                option.textContent = building.name;
                select.appendChild(option);
            });
        });
        
        console.log('Building dropdowns populated with', buildings.length, 'options');
    } catch (error) {
        console.error('Error loading buildings:', error);
    }
}

// Load floors by building
async function loadFloors() {
    console.log('loadFloors function called');
    
    const buildingSelect = document.getElementById('building');
    const floorSelect = document.getElementById('floor');
    
    console.log('Building select found:', !!buildingSelect);
    console.log('Floor select found:', !!floorSelect);
    
    if (!buildingSelect || !floorSelect) {
        console.log('Building or floor select not found');
        return;
    }
    
    const selectedBuilding = buildingSelect.value;
    console.log('Building selected:', selectedBuilding);
    
    if (!selectedBuilding) {
        floorSelect.innerHTML = '<option value="">Select floor</option>';
        console.log('No building selected, clearing floor dropdown');
        return;
    }
   
    const building = buildings.find(b => b.name === selectedBuilding);
    if (!building) {
        console.log('Building not found in buildings array');
        console.log('Available buildings:', buildings.map(b => b.name));
        return;
    }
    
    console.log('Loading floors for building:', building);
    
    try {
        const data = await makeAPIRequest(`/floors/${building.id}`);
        const floors = data.floors;
        console.log('Floors loaded:', floors);
        
        // Sort floors: Ground Floor first, then 1-27, then Background Floor
        const sortedFloors = floors.sort((a, b) => {
            if (a.label === 'Ground Floor') return -1;
            if (b.label === 'Ground Floor') return 1;
            if (a.label === 'Background Floor') return 1;
            if (b.label === 'Background Floor') return -1;
            
            // For numeric floors, sort numerically
            const aNum = parseInt(a.label);
            const bNum = parseInt(b.label);
            if (!isNaN(aNum) && !isNaN(bNum)) {
                return aNum - bNum;
            }
            
            return a.label.localeCompare(b.label);
        });
        
        console.log('Sorted floors:', sortedFloors.map(f => f.label));
        
        // Populate floor dropdown
        floorSelect.innerHTML = '<option value="">Select floor</option>';
        sortedFloors.forEach(floor => {
            const option = document.createElement('option');
            option.value = floor.label;
            option.textContent = floor.label;
            floorSelect.appendChild(option);
        });
        
        console.log('Floor dropdown populated with', sortedFloors.length, 'options');
        
      
        console.log('Loading departments after floors...');
        loadAllDepartments();
    } catch (error) {
        console.error('Error loading floors:', error);
    }
}

// Load all departments
async function loadAllDepartments() {
    try {
        console.log('Loading departments...');
        const data = await makeAPIRequest('/departments');
        departments = data.departments;
        console.log('Departments loaded:', departments);
        
        // Populate department dropdown
        const departmentSelect = document.getElementById('department');
        if (departmentSelect) {
            console.log('Found department select, populating...');
            departmentSelect.innerHTML = '<option value="">Select Department</option>';
            departments.forEach(dept => {
                const option = document.createElement('option');
                option.value = dept.name;
                option.textContent = dept.name;
                departmentSelect.appendChild(option);
            });
            console.log('Department dropdown populated with', departments.length, 'options');
        } else {
            console.log('Department select element not found');
        }
    } catch (error) {
        console.error('Error loading departments:', error);
    }
}

// Load departments by building
async function loadDepartmentsByBuilding(buildingName) {
    try {
        const data = await makeAPIRequest(`/departments/${encodeURIComponent(buildingName)}`);
        const buildingDepts = data.departments;
        
        const departmentSelect = document.getElementById('department');
        if (departmentSelect) {
            departmentSelect.innerHTML = '<option value="">Select Department</option>';
            buildingDepts.forEach(dept => {
                const option = document.createElement('option');
                option.value = dept.name;
                option.textContent = dept.name;
                departmentSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading departments by building:', error);
    }
}

// Load tickets
async function loadTickets() {
    if (!isLoggedIn) return;
    
    try {
        const data = await makeAPIRequest('/tickets');
        tickets = data.tickets;
        displayTickets(tickets);
    } catch (error) {
        console.error('Error loading tickets:', error);
    }
}

// Load dashboard
async function loadDashboard() {
    if (!isLoggedIn) return;
    
    try {
        const data = await makeAPIRequest('/dashboard');
        updateDashboardStats(data);
        updateHomeKPIs(data);
        displayRecentTickets(data.recent_tickets);
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

// Update dashboard statistics
function updateDashboardStats(data) {
    const stats = data.status_counts;
    const priorities = data.priority_counts;
    const total = data.total_tickets || 1; // Prevent division by zero
    
    // Update stat cards with animations
    animateStatCard('total-tickets', data.total_tickets, 100);
    animateStatCard('pending-tickets', stats.pending || 0, ((stats.pending || 0) / total) * 100);
    animateStatCard('in-progress-tickets', stats.in_progress || 0, ((stats.in_progress || 0) / total) * 100);
    animateStatCard('resolved-tickets', stats.resolved || 0, ((stats.resolved || 0) / total) * 100);
    animateStatCard('closed-tickets', stats.closed || 0, ((stats.closed || 0) / total) * 100);
    
    // Update tickets count
    const ticketsCountEl = document.getElementById('tickets-count');
    if (ticketsCountEl) {
        ticketsCountEl.textContent = `${data.total_tickets || 0} tickets`;
    }
}

// Animate stat cards with progress bars
function animateStatCard(cardId, value, progressPercent) {
    const card = document.getElementById(cardId);
    if (!card) return;
    
    const valueEl = card.querySelector('h3');
    const progressFill = card.querySelector('.progress-fill');
    
    // Animate number
    let currentValue = 0;
    const increment = value / 30; // 30 frames for smooth animation
    const numberAnimation = setInterval(() => {
        currentValue += increment;
        if (currentValue >= value) {
            currentValue = value;
            clearInterval(numberAnimation);
        }
        valueEl.textContent = Math.floor(currentValue);
    }, 50);
    
    // Animate progress bar
    setTimeout(() => {
        if (progressFill) {
            progressFill.style.width = `${Math.min(progressPercent, 100)}%`;
        }
    }, 200);
}

// Display tickets
let currentTicket = null;

function displayTickets(ticketsToShow) {
    const container = document.getElementById('all-tickets');
    if (!container) return;
    
    if (ticketsToShow.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">
                    <i class="fas fa-ticket-alt"></i>
                </div>
                <h3>No tickets found</h3>
                <p>Try adjusting your filters or create a new ticket</p>
                <button class="btn btn-primary" onclick="showSection('create-ticket')">
                    <i class="fas fa-plus"></i> Create New Ticket
                </button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = ticketsToShow.map(ticket => {
        // Check if ticket is resolved or closed for rating
        const isRatable = ticket.status === 'resolved' || ticket.status === 'closed';
        
        return `
        <div class="ticket-card" data-ticket-id="${ticket.id}">
            <div class="ticket-header">
                <div class="ticket-info">
                    <div class="ticket-title">${ticket.issue_type}</div>
                    <div class="ticket-priority ${ticket.priority || 'medium'}">
                        <i class="fas fa-flag"></i>
                        ${ticket.priority || 'medium'}
                    </div>
                </div>
                <div class="ticket-status ${ticket.status}">
                    <span class="status-dot"></span>
                    ${ticket.status.replace('_', ' ')}
                </div>
            </div>
            <div class="ticket-details">
                <div class="ticket-detail">
                    <i class="fas fa-building"></i>
                    <span>${ticket.building_name || 'Unknown'} - Floor ${ticket.floor_label || 'Unknown'}</span>
                </div>
                <div class="ticket-detail">
                    <i class="fas fa-users"></i>
                    <span>${ticket.department_name || 'Unknown'}</span>
                </div>
                <div class="ticket-detail">
                    <i class="fas fa-user"></i>
                    <span>${ticket.contact_person || 'Not specified'}</span>
                </div>
                <div class="ticket-detail">
                    <i class="fas fa-calendar"></i>
                    <span>${formatDate(ticket.created_at)}</span>
                </div>
            </div>
            <div class="ticket-description">
                ${ticket.description.length > 100 ? ticket.description.substring(0, 100) + '...' : ticket.description}
            </div>
            ${ticket.notification ? `<div class="ticket-notification">
                <i class="fas fa-bell"></i>
                <span>${ticket.notification}</span>
            </div>` : ''}
            <div class="ticket-actions">
                <button class="btn btn-sm btn-primary" onclick="openTicketModal(${ticket.id})">
                    <i class="fas fa-eye"></i> View
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteTicket(${ticket.id})">
                    <i class="fas fa-trash"></i> Delete
                </button>
                ${isRatable ? `
                    <button class="btn btn-sm btn-warning" onclick="showRatingModal(${ticket.id})" style="background-color: #FFC000; color: white; border: none;">
                        <i class="fas fa-star"></i> Rate Service
                    </button>
                ` : ''}
            </div>
            ${isRatable && ticket.rating ? `
                <div class="ticket-rating-display" style="text-align: right; margin-top: 10px; padding: 8px; background: rgba(255, 192, 0, 0.1); border-radius: 4px;">
                    <span style="color: #FFC000; font-size: 16px;">
                        ${'★'.repeat(ticket.rating)}${'☆'.repeat(5-ticket.rating)}
                    </span>
                    ${ticket.rating_comment ? `<div style="font-size: 12px; color: #666; margin-top: 5px;">"${ticket.rating_comment}"</div>` : ''}
                </div>
            ` : ''}
        </div>
    `}).join('');
}

// Display recent tickets
function displayRecentTickets(recentTickets) {
    const container = document.getElementById('recent-tickets');
    if (!container) return;
    
    if (!recentTickets || recentTickets.length === 0) {
        container.innerHTML = '<div class="loading">No recent tickets.</div>';
        return;
    }
    
    container.innerHTML = recentTickets.map(ticket => {
        const isRatable = ticket.status === 'resolved' || ticket.status === 'closed';
        
        return `
        <div class="ticket-card">
            <div class="ticket-header">
                <div class="ticket-title">${ticket.issue_type}</div>
                <div class="ticket-status ${ticket.status}">${ticket.status.replace('_', ' ')}</div>
            </div>
            <div class="ticket-details">
                <div class="ticket-detail">
                    <i class="fas fa-building"></i>
                    <span>${ticket.building_name || 'Unknown'} - Floor ${ticket.floor_label || 'Unknown'}</span>
                </div>
                <div class="ticket-detail">
                    <i class="fas fa-calendar"></i>
                    <span>${new Date(ticket.created_at).toLocaleDateString()}</span>
                </div>
            </div>
            <div class="ticket-actions">
                <button class="btn btn-sm btn-primary" onclick="openTicketModal(${ticket.id})">
                    <i class="fas fa-eye"></i> View
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteTicket(${ticket.id})">
                    <i class="fas fa-trash"></i> Delete
                </button>
                ${isRatable ? `
                    <button class="btn btn-sm btn-warning" onclick="showRatingModal(${ticket.id})" style="background-color: #FFC000; color: white; border: none;">
                        <i class="fas fa-star"></i> Rate Service
                    </button>
                ` : ''}
            </div>
            ${isRatable && ticket.rating ? `
                <div class="ticket-rating-display" style="text-align: right; margin-top: 10px; padding: 8px; background: rgba(255, 192, 0, 0.1); border-radius: 4px;">
                    <span style="color: #FFC000; font-size: 16px;">
                        ${'★'.repeat(ticket.rating)}${'☆'.repeat(5-ticket.rating)}
                    </span>
                    ${ticket.rating_comment ? `<div style="font-size: 12px; color: #666; margin-top: 5px;">"${ticket.rating_comment}"</div>` : ''}
                </div>
            ` : ''}
        </div>
    `}).join('');
}

// Handle ticket form submission
async function handleTicketSubmission(event) {
    event.preventDefault();
    
    if (!isLoggedIn) {
        showNotification('Please login to create tickets.', 'error');
        return;
    }
    
    const formData = new FormData(event.target);
    const ticketData = {
        building: formData.get('building'),
        floor: formData.get('floor'),
        department: formData.get('department'),
        issue_type: formData.get('issue_type'),
        description: formData.get('description'),
        contact_person: formData.get('contact_person'),
        phone_number: formData.get('phone_number'),
        priority: formData.get('priority'),
        user_id: currentUser.id
    };
    
    try {
        const response = await makeAPIRequest('/tickets', {
            method: 'POST',
            body: JSON.stringify(ticketData)
        });
        
        showNotification('Ticket created successfully!', 'success');
        resetForm();
        
        // Refresh tickets and dashboard
        await loadTickets();
        await loadDashboard();
        
    } catch (error) {
        console.error('Error creating ticket:', error);
        showNotification('Error creating ticket. Please try again.', 'error');
    }
}

// Reset form
function resetForm() {
    document.getElementById('ticket-form').reset();
    document.getElementById('department').innerHTML = '<option value="">Select Department</option>';
}

// Load departments when building is selected
function loadDepartments() {
    const buildingSelect = document.getElementById('building');
    const selectedBuilding = buildingSelect.value;
    
    if (selectedBuilding) {
        loadDepartmentsByBuilding(selectedBuilding);
    } else {
        document.getElementById('department').innerHTML = '<option value="">Select Department</option>';
    }
}

// Filter tickets
function filterTickets() {
    const statusFilter = document.getElementById('status-filter').value;
    const buildingFilter = document.getElementById('building-filter').value;
    const searchFilter = document.getElementById('search-filter').value.toLowerCase();
    
    let filteredTickets = tickets;
    
    if (statusFilter) {
        filteredTickets = filteredTickets.filter(ticket => ticket.status === statusFilter);
    }
    
    if (buildingFilter) {
        filteredTickets = filteredTickets.filter(ticket => ticket.building === buildingFilter);
    }
    
    if (searchFilter) {
        filteredTickets = filteredTickets.filter(ticket => 
            ticket.description.toLowerCase().includes(searchFilter) ||
            ticket.contact_person.toLowerCase().includes(searchFilter) ||
            ticket.issue_type.toLowerCase().includes(searchFilter)
        );
    }
    
    displayTickets(filteredTickets);
}

// Chat functions
function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    input.value = '';
    
    // Show typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai-message typing';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <p>GPO is thinking...</p>
        </div>
    `;
    document.getElementById('chat-messages').appendChild(typingDiv);
    
    // Scroll to bottom
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    try {
        const response = await makeAPIRequest('/ai/chat', {
            method: 'POST',
            body: JSON.stringify({ message })
        });
        
        typingDiv.remove();
        
        addMessageToChat(response.response, 'ai');
        
    } catch (error) {
        // Remove typing indicator
        typingDiv.remove();
        
        console.error('Error sending message:', error);
        
        let errorMessage = 'I\'m here to help! Please try asking your question again.';
        if (error.name === 'TimeoutError') {
            errorMessage = 'I\'m a bit busy right now, but I can still help! Please try asking your question again.';
        } else if (error.message.includes('429')) {
            errorMessage = 'I\'m getting a lot of requests right now. Please try again in a moment.';
        }
        
        addMessageToChat(errorMessage, 'ai');
    }
}

function addMessageToChat(message, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerHTML = `<p>${message}</p>`;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function askQuestion(question) {
    const input = document.getElementById('chat-input');
    input.value = question;
    sendMessage();
}

function showNotification(message, type = 'success', title = '') {
    const notification = document.getElementById('notification');
    const messageEl = notification.querySelector('.notification-message');
    const titleEl = notification.querySelector('.notification-title');
    const iconEl = notification.querySelector('.notification-icon');
    

    if (title) {
        titleEl.textContent = title;
        titleEl.style.display = 'block';
    } else {
        titleEl.style.display = 'none';
    }
    messageEl.textContent = message;
    
    notification.className = `notification ${type}`;
    const icons = {
        success: '<i class="fas fa-check"></i>',
        error: '<i class="fas fa-exclamation-triangle"></i>',
        warning: '<i class="fas fa-exclamation-circle"></i>',
        info: '<i class="fas fa-info-circle"></i>'
    };
    iconEl.innerHTML = icons[type] || icons.success;
    
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 5000);
    
    notification.onclick = () => {
        notification.classList.remove('show');
    };
}


function refreshDashboard() {
    if (!isLoggedIn) {
        showNotification('Please login to view dashboard.', 'error');
        return;
    }
    loadDashboard();
    showNotification('Dashboard refreshed!', 'success');
}


function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}


window.addEventListener('error', function(event) {
    console.error('Global error:', event.error);
    showNotification('An error occurred. Please refresh the page.', 'error');
});

function openTicketModal(ticketId) {
    const ticket = tickets.find(t => t.id === ticketId);
    if (!ticket) {
        showNotification('Ticket not found', 'error');
        return;
    }
    
    currentTicket = ticket;
    const modal = document.getElementById('ticket-modal');
    const modalBody = document.getElementById('modal-body');
    
    modalBody.innerHTML = `
        <div class="ticket-modal-content">
            <div class="ticket-modal-header">
                <div class="ticket-modal-title">
                    <h4>${ticket.issue_type}</h4>
                    <div class="ticket-modal-status">
                        <span class="status-badge ${ticket.status}">
                            <span class="status-dot"></span>
                            ${ticket.status.replace('_', ' ')}
                        </span>
                        <span class="priority-badge ${ticket.priority || 'medium'}">
                            <i class="fas fa-flag"></i>
                            ${ticket.priority || 'medium'}
                        </span>
                    </div>
                </div>
            </div>
            
            <div class="ticket-modal-details">
                <div class="detail-row">
                    <div class="detail-item">
                        <label><i class="fas fa-building"></i> Location</label>
                        <span>${ticket.building_name || 'Unknown'} - Floor ${ticket.floor_label || 'Unknown'}</span>
                    </div>
                    <div class="detail-item">
                        <label><i class="fas fa-users"></i> Department</label>
                        <span>${ticket.department_name || 'Unknown'}</span>
                    </div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-item">
                        <label><i class="fas fa-user"></i> Contact Person</label>
                        <span>${ticket.contact_person || 'Not specified'}</span>
                    </div>
                    <div class="detail-item">
                        <label><i class="fas fa-phone"></i> Phone Number</label>
                        <span>${ticket.phone_number || 'Not specified'}</span>
                    </div>
                </div>
                
                <div class="detail-row">
                    <div class="detail-item">
                        <label><i class="fas fa-calendar"></i> Created</label>
                        <span>${formatDate(ticket.created_at)}</span>
                    </div>
                    <div class="detail-item">
                        <label><i class="fas fa-clock"></i> Last Updated</label>
                        <span>${formatDate(ticket.updated_at || ticket.created_at)}</span>
                    </div>
                </div>
            </div>
            
            <div class="ticket-modal-description">
                <label><i class="fas fa-comment-alt"></i> Description</label>
                <div class="description-content">
                    ${ticket.description}
                </div>
            </div>
            
            ${ticket.notification ? `
            <div class="ticket-modal-notification">
                <label><i class="fas fa-bell"></i> Notification</label>
                <div class="notification-content">
                    ${ticket.notification}
                </div>
            </div>
            ` : ''}
            
            <div class="ticket-modal-actions">
                <button class="btn btn-danger" onclick="deleteTicket(${ticket.id})">
                    <i class="fas fa-trash"></i> Delete Ticket
                </button>
            </div>
        </div>
    `;
    
    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeTicketModal() {
    const modal = document.getElementById('ticket-modal');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
    currentTicket = null;
}

async function deleteTicket(ticketId) {
    if (!currentUser) {
        showNotification('Please login to delete tickets.', 'error');
        return;
    }
    
    const ticket = tickets.find(t => t.id === ticketId);
    if (!ticket) {
        showNotification('Ticket not found', 'error');
        return;
    }
    
    if (!confirm(`Are you sure you want to delete this ticket?\n\nIssue: ${ticket.issue_type}\nStatus: ${ticket.status}`)) {
        return;
    }
    
    try {
        await makeAPIRequest(`/tickets/${ticketId}`, {
            method: 'DELETE'
        });
        
        showNotification('Ticket deleted successfully!', 'success');
        
        if (currentTicket && currentTicket.id === ticketId) {
            closeTicketModal();
        }
        
        await loadTickets();
        await loadDashboard();
        
    } catch (error) {
        console.error('Error deleting ticket:', error);
        showNotification('Failed to delete ticket. Please try again.', 'error');
    }
}

function refreshTickets() {
    if (!isLoggedIn) {
        showNotification('Please login to view tickets.', 'error');
        return;
    }
    loadTickets();
    showNotification('Tickets refreshed!', 'success');
}

document.addEventListener('click', function(event) {
    const modal = document.getElementById('ticket-modal');
    if (event.target === modal) {
        closeTicketModal();
    }
    
    const ratingModal = document.getElementById('rating-modal');
    if (event.target === ratingModal) {
        closeRatingModal();
    }
});

let currentRatingTicketId = null;
let currentRating = 0;

function showRatingModal(ticketId) {
    currentRatingTicketId = ticketId;
    currentRating = 0;
    
    // Create and show modal
    const modalHTML = `
        <div id="rating-modal" class="modal" style="display: flex; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; align-items: center; justify-content: center;">
            <div class="modal-content" style="background: white; padding: 30px; border-radius: 10px; max-width: 500px; width: 90%;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h3 style="margin: 0; color: #333;">
                        <i class="fas fa-star" style="color: #FFC000;"></i> Rate Our Service
                    </h3>
                    <button onclick="closeRatingModal()" style="background: none; border: none; font-size: 20px; cursor: pointer; color: #666;">&times;</button>
                </div>
                
                <p style="margin-bottom: 20px; color: #666;">How would you rate the service for this ticket?</p>
                
                <div class="stars-container" style="display: flex; justify-content: center; gap: 10px; margin-bottom: 20px;">
                    <span class="star" data-rating="1" style="font-size: 30px; color: #ddd; cursor: pointer;">☆</span>
                    <span class="star" data-rating="2" style="font-size: 30px; color: #ddd; cursor: pointer;">☆</span>
                    <span class="star" data-rating="3" style="font-size: 30px; color: #ddd; cursor: pointer;">☆</span>
                    <span class="star" data-rating="4" style="font-size: 30px; color: #ddd; cursor: pointer;">☆</span>
                    <span class="star" data-rating="5" style="font-size: 30px; color: #ddd; cursor: pointer;">☆</span>
                </div>
                
                <div id="rating-text" style="text-align: center; margin-bottom: 20px; color: #666; font-size: 14px;">Select a rating</div>
                
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 8px; color: #333; font-weight: bold;">Additional Comments (Optional):</label>
                    <textarea id="rating-comment" placeholder="Share your experience with our service..." style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; resize: vertical; min-height: 80px;"></textarea>
                </div>
                
                <div style="display: flex; gap: 10px; justify-content: center;">
                    <button onclick="closeRatingModal()" class="btn btn-secondary" style="padding: 10px 20px; border: 1px solid #ddd; background: #f8f9fa; border-radius: 4px; cursor: pointer;">Cancel</button>
                    <button onclick="submitRating()" id="submit-rating-btn" disabled class="btn btn-primary" style="padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; opacity: 0.5;">Submit Rating</button>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('rating-modal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to body
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Setup star listeners
    setupStarListeners();
}

// Setup star click listeners
function setupStarListeners() {
    const stars = document.querySelectorAll('.star');
    
    stars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = parseInt(this.getAttribute('data-rating'));
            currentRating = rating;
            
            // Update stars
            stars.forEach((s, i) => {
                if (i < rating) {
                    s.textContent = '★';
                    s.style.color = '#FFC000';
                } else {
                    s.textContent = '☆';
                    s.style.color = '#ddd';
                }
            });
            
            // Update text
            const ratingTexts = ['', 'Poor', 'Fair', 'Good', 'Very Good', 'Excellent'];
            document.getElementById('rating-text').textContent = ratingTexts[rating];
            
            // Enable submit button
            document.getElementById('submit-rating-btn').disabled = false;
            document.getElementById('submit-rating-btn').style.opacity = '1';
        });
        
        star.addEventListener('mouseenter', function() {
            const rating = parseInt(this.getAttribute('data-rating'));
            stars.forEach((s, i) => {
                if (i < rating) {
                    s.textContent = '★';
                    s.style.color = '#FFC000';
                } else {
                    s.textContent = '☆';
                    s.style.color = '#ddd';
                }
            });
        });
        
        star.addEventListener('mouseleave', function() {
            stars.forEach((s, i) => {
                if (i < currentRating) {
                    s.textContent = '★';
                    s.style.color = '#FFC000';
                } else {
                    s.textContent = '☆';
                    s.style.color = '#ddd';
                }
            });
        });
    });
}

function closeRatingModal() {
    const modal = document.getElementById('rating-modal');
    if (modal) {
        modal.remove();
    }
    currentRatingTicketId = null;
    currentRating = 0;
}


async function submitRating() {
    if (!currentRating || !currentRatingTicketId) {
        showNotification('Please select a rating', 'error');
        return;
    }
    
    const comment = document.getElementById('rating-comment').value.trim();
    
    try {
        const response = await makeAPIRequest(`/tickets/${currentRatingTicketId}/rate`, {
            method: 'POST',
            body: JSON.stringify({
                rating: currentRating,
                comment: comment
            })
        });
        
        showNotification('Rating submitted successfully!', 'success');
        closeRatingModal();
        
        await loadTickets();
        await loadDashboard();
        
    } catch (error) {
        console.error('Error submitting rating:', error);
        showNotification('Failed to submit rating. Please try again.', 'error');
    }
}

function showEmergencyModal() {
    const modal = document.getElementById('emergency-modal');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        
        modal.querySelector('.modal-content').style.animation = 'modalSlideIn 0.3s ease';
    }
}

function closeEmergencyModal() {
    const modal = document.getElementById('emergency-modal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function callEmergency() {
    window.open('tel:0702248984', '_self');
    showNotification('Opening phone dialer...', 'info');
}

function emailEmergency() {
    const subject = encodeURIComponent('URGENT: ICT Emergency Support Required');
    const body = encodeURIComponent(`Dear ICT Support Team,\n\nThis is an emergency request for immediate assistance.\n\nIssue Description:\n\nLocation:\n\nContact Number:\n\nThank you.`);
    window.open(`mailto:emergency@ict.go.ke?subject=${subject}&body=${body}`, '_self');
    showNotification('Opening email client...', 'info');
}

function whatsappEmergency() {
    // Open WhatsApp with emergency message
    const message = encodeURIComponent('🚨 URGENT: ICT Emergency Support Required\n\nHello, I need immediate ICT support assistance. This is an emergency situation.\n\nPlease respond as soon as possible.\n\nThank you.');
    const phoneNumber = '254702248984'; // WhatsApp format with country code
    window.open(`https://wa.me/${phoneNumber}?text=${message}`, '_blank');
    showNotification('Opening WhatsApp...', 'info');
}

function chatEmergency() {
    // Redirect to AI chat with emergency context
    showSection('ai-assistant');
    closeEmergencyModal();
    
    // Auto-fill emergency message
    setTimeout(() => {
        const chatInput = document.getElementById('chat-input');
        if (chatInput) {
            chatInput.value = 'URGENT: I need immediate ICT support assistance. This is an emergency situation.';
            sendMessage();
        }
    }, 500);
    
    showNotification('Redirecting to AI Assistant for emergency support...', 'info');
}

function createEmergencyTicket() {
    // Create a high-priority emergency ticket
    closeEmergencyModal();
    showSection('create-ticket');
    
    // Auto-fill emergency ticket details
    setTimeout(() => {
        const issueTypeSelect = document.getElementById('issue_type');
        const prioritySelect = document.getElementById('priority');
        const descriptionTextarea = document.getElementById('description');
        
        if (issueTypeSelect) issueTypeSelect.value = 'Emergency';
        if (prioritySelect) prioritySelect.value = 'urgent';
        if (descriptionTextarea) {
            descriptionTextarea.value = 'EMERGENCY: This is an urgent ICT support request requiring immediate attention.';
        }
        
        showNotification('Emergency ticket form prepared. Please fill in the details.', 'warning');
    }, 500);
}

// Close emergency modal when clicking outside
document.addEventListener('click', function(event) {
    const emergencyModal = document.getElementById('emergency-modal');
    if (event.target === emergencyModal) {
        closeEmergencyModal();
    }
});