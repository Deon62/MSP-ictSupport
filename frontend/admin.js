class AdminModule {
    constructor() {
        this.token = localStorage.getItem('admin_token');
        this.user = JSON.parse(localStorage.getItem('admin_user') || '{}');
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuthStatus();
        this.loadAIHealthStatus();
    }

    setupEventListeners() {
    
        document.getElementById('login-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        
        document.getElementById('password-form')?.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handlePasswordChange();
        });

      
        document.querySelectorAll('.nav-item[data-section]').forEach(item => {
            item.addEventListener('click', (e) => {
                this.showSection(e.target.dataset.section);
            });
        });
    }

    async handleLogin() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (response.ok) {
                this.token = data.token;
                this.user = data.user;
                
                localStorage.setItem('admin_token', this.token);
                localStorage.setItem('admin_user', JSON.stringify(this.user));

                if (data.must_change_password) {
                    this.showPasswordChangeForm();
                } else {
                    this.showAdminDashboard();
                }
            } else {
                this.showErrorMessage(data.message || 'Login failed');
            }
        } catch (error) {
            this.showErrorMessage('Network error. Please try again.');
        }
    }

    async handlePasswordChange() {
        const currentPassword = document.getElementById('current-password').value;
        const newPassword = document.getElementById('new-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        if (newPassword !== confirmPassword) {
            this.showErrorMessage('New passwords do not match');
            return;
        }

        try {
            const response = await fetch('/api/change-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({
                    current_password: currentPassword,
                    new_password: newPassword
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.showSuccessMessage('Password changed successfully');
                document.getElementById('password-change').classList.remove('active');
                this.showAdminDashboard();
            } else {
                this.showErrorMessage(data.message || 'Password change failed');
            }
        } catch (error) {
            this.showErrorMessage('Network error. Please try again.');
        }
    }

    checkAuthStatus() {
        if (this.token && this.user.id) {
            this.showAdminDashboard();
            this.loadData();
        } else {
            this.showLoginForm();
        }
    }

    showLoginForm() {
        document.getElementById('login-section').style.display = 'flex';
        document.getElementById('admin-dashboard').classList.remove('active');
    }

    showAdminDashboard() {
        document.getElementById('login-section').style.display = 'none';
        document.getElementById('admin-dashboard').classList.add('active');
        this.loadData();
    }

    showPasswordChangeForm() {
        document.getElementById('password-change').classList.add('active');
    }

    showSection(sectionName) {
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-section="${sectionName}"]`).classList.add('active');

      
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(`${sectionName}-section`).classList.add('active');

       
        const titles = {
            'tickets': 'Tickets',
            'departments': 'Departments',
            'buildings': 'Buildings & Floors',
            'users': 'Team Members',
            'settings': 'Settings'
        };
        document.getElementById('section-title').textContent = titles[sectionName] || 'Admin';

        // Load section data
        this.loadSectionData(sectionName);
    }

    async loadData() {
        await Promise.all([
            this.loadTickets(),
            this.loadDepartments(),
            this.loadBuildings(),
            this.loadUsers()
        ]);
    }

    async loadSectionData(section) {
        switch (section) {
            case 'tickets':
                await this.loadTickets();
                break;
            case 'departments':
                await this.loadDepartments();
                break;
            case 'buildings':
                await this.loadBuildings();
                break;
            case 'users':
                await this.loadUsers();
                break;
        }
    }

    async loadTickets() {
        const loading = document.getElementById('tickets-loading');
        const table = document.getElementById('tickets-table');

        loading.classList.add('active');
        table.innerHTML = '';

        try {
            const response = await fetch('/api/admin/tickets', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.renderTicketsTable(data.tickets || []);
                this.updateTicketStats(data.tickets || []);
            } else {
                table.innerHTML = '<p style="padding: 20px; color: #666;">Failed to load tickets</p>';
            }
        } catch (error) {
            table.innerHTML = '<p style="padding: 20px; color: #666;">Error loading tickets</p>';
        } finally {
            loading.classList.remove('active');
        }
    }

    async loadDepartments() {
        const loading = document.getElementById('departments-loading');
        const table = document.getElementById('departments-table');

        loading.classList.add('active');
        table.innerHTML = '';

        try {
            const response = await fetch('/api/admin/departments', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.renderDepartmentsTable(data.departments || []);
            } else {
                table.innerHTML = '<p style="padding: 20px; color: #666;">Failed to load departments</p>';
            }
        } catch (error) {
            table.innerHTML = '<p style="padding: 20px; color: #666;">Error loading departments</p>';
        } finally {
            loading.classList.remove('active');
        }
    }

    async loadBuildings() {
        const loading = document.getElementById('buildings-loading');
        const table = document.getElementById('buildings-table');

        loading.classList.add('active');
        table.innerHTML = '';

        try {
            const response = await fetch('/api/admin/buildings', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.renderBuildingsTable(data.buildings || []);
            } else {
                table.innerHTML = '<p style="padding: 20px; color: #666;">Failed to load buildings</p>';
            }
        } catch (error) {
            table.innerHTML = '<p style="padding: 20px; color: #666;">Error loading buildings</p>';
        } finally {
            loading.classList.remove('active');
        }
    }

    async loadUsers() {
        const loading = document.getElementById('users-loading');
        const table = document.getElementById('users-table');

        loading.classList.add('active');
        table.innerHTML = '';

        try {
            const response = await fetch('/api/admin/users', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                this.renderUsersTable(data.users || []);
            } else {
                table.innerHTML = '<p style="padding: 20px; color: #666;">Failed to load users</p>';
            }
        } catch (error) {
            table.innerHTML = '<p style="padding: 20px; color: #666;">Error loading users</p>';
        } finally {
            loading.classList.remove('active');
        }
    }

    renderTicketsTable(tickets) {
        const table = document.getElementById('tickets-table');
        
        if (tickets.length === 0) {
            table.innerHTML = '<p style="padding: 20px; color: #666;">No tickets found</p>';
            return;
        }

        const html = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Issue</th>
                        <th>Building</th>
                        <th>Department</th>
                        <th>Status</th>
                        <th>Priority</th>
                        <th>Created</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${tickets.map(ticket => `
                        <tr>
                            <td>#${ticket.id}</td>
                            <td>${ticket.issue_type}</td>
                            <td>${ticket.building_name || 'N/A'}</td>
                            <td>${ticket.department_name || 'N/A'}</td>
                            <td>
                                <span class="status-badge status-${ticket.status}">
                                    ${ticket.status.replace('_', ' ')}
                                </span>
                            </td>
                            <td>${ticket.priority}</td>
                            <td>${new Date(ticket.created_at).toLocaleDateString()}</td>
                            <td>
                                <select onchange="adminModule.updateTicketStatus(${ticket.id}, this.value)">
                                    <option value="">Change Status</option>
                                    <option value="pending">Pending</option>
                                    <option value="in_progress">In Progress</option>
                                    <option value="resolved">Resolved</option>
                                    <option value="closed">Closed</option>
                                </select>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        table.innerHTML = html;
    }

    renderDepartmentsTable(departments) {
        const table = document.getElementById('departments-table');
        
        if (departments.length === 0) {
            table.innerHTML = '<p style="padding: 20px; color: #666;">No departments found</p>';
            return;
        }

        const html = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Created</th>
                    </tr>
                </thead>
                <tbody>
                    ${departments.map(dept => `
                        <tr>
                            <td>${dept.id}</td>
                            <td>${dept.name}</td>
                            <td>${dept.description || 'N/A'}</td>
                            <td>${new Date(dept.created_at).toLocaleDateString()}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        table.innerHTML = html;
    }

    renderBuildingsTable(buildings) {
        const table = document.getElementById('buildings-table');
        
        if (buildings.length === 0) {
            table.innerHTML = '<p style="padding: 20px; color: #666;">No buildings found</p>';
            return;
        }

        const html = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Floors</th>
                    </tr>
                </thead>
                <tbody>
                    ${buildings.map(building => `
                        <tr>
                            <td>${building.id}</td>
                            <td>${building.name}</td>
                            <td>${building.description || 'N/A'}</td>
                            <td>${building.floors_count || 0}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        table.innerHTML = html;
    }

    renderUsersTable(users) {
        const table = document.getElementById('users-table');
        
        if (users.length === 0) {
            table.innerHTML = '<p style="padding: 20px; color: #666;">No users found</p>';
            return;
        }

        const html = `
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Username</th>
                        <th>Role</th>
                        <th>Department</th>
                        <th>Status</th>
                        <th>Last Login</th>
                    </tr>
                </thead>
                <tbody>
                    ${users.map(user => `
                        <tr>
                            <td>${user.id}</td>
                            <td>${user.username}</td>
                            <td>
                                <span class="role-badge role-${user.role.toLowerCase()}">
                                    ${user.role}
                                </span>
                            </td>
                            <td>${user.department_name || 'N/A'}</td>
                            <td>
                                <span class="status-badge ${user.active ? 'status-resolved' : 'status-closed'}">
                                    ${user.active ? 'Active' : 'Inactive'}
                                </span>
                            </td>
                            <td>${user.last_login ? new Date(user.last_login).toLocaleDateString() : 'Never'}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        table.innerHTML = html;
    }

    updateTicketStats(tickets) {
        const stats = {
            total: tickets.length,
            open: tickets.filter(t => t.status === 'pending').length,
            inProgress: tickets.filter(t => t.status === 'in_progress').length,
            resolved: tickets.filter(t => t.status === 'resolved').length
        };

        document.getElementById('total-tickets').textContent = stats.total;
        document.getElementById('open-tickets').textContent = stats.open;
        document.getElementById('in-progress-tickets').textContent = stats.inProgress;
        document.getElementById('resolved-tickets').textContent = stats.resolved;
    }

    async updateTicketStatus(ticketId, status) {
        if (!status) return;

        try {
            const response = await fetch(`/api/admin/tickets/${ticketId}/status`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({ status })
            });

            if (response.ok) {
                this.showSuccessMessage('Ticket status updated');
                this.loadTickets();
            } else {
                const data = await response.json();
                this.showErrorMessage(data.message || 'Failed to update ticket status');
            }
        } catch (error) {
            this.showErrorMessage('Network error. Please try again.');
        }
    }

    async loadAIHealthStatus() {
        try {
            const response = await fetch('/api/health/ai');
            const data = await response.json();
            
            const statusElement = document.getElementById('ai-status');
            if (data.status === 'ok') {
                statusElement.textContent = '🤖 AI Assistant: Online';
                statusElement.className = 'ai-status online';
            } else {
                statusElement.textContent = '🤖 AI Assistant: Offline';
                statusElement.className = 'ai-status offline';
                statusElement.title = data.error || 'AI service unavailable';
            }
        } catch (error) {
            const statusElement = document.getElementById('ai-status');
            statusElement.textContent = '🤖 AI Assistant: Error';
            statusElement.className = 'ai-status offline';
        }
    }

    showSuccessMessage(message) {
        this.showToast(message, 'success');
    }

    showErrorMessage(message) {
        this.showToast(message, 'error');
    }

    showToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => toast.classList.add('show'), 100);
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => document.body.removeChild(toast), 300);
        }, 3000);
    }

    logout() {
        localStorage.removeItem('admin_token');
        localStorage.removeItem('admin_user');
        this.token = null;
        this.user = {};
        this.showLoginForm();
    }
}

// Global functions for button clicks
function logout() {
    adminModule.logout();
}

function refreshTickets() {
    adminModule.loadTickets();
}

function addDepartment() {
    adminModule.showErrorMessage('Add department functionality coming soon');
}

function addBuilding() {
    adminModule.showErrorMessage('Add building functionality coming soon');
}

function addUser() {
    adminModule.showErrorMessage('Add user functionality coming soon');
}

function checkAIHealth() {
    adminModule.loadAIHealthStatus();
    adminModule.showSuccessMessage('AI health check completed');
}

// Initialize admin module when page loads
let adminModule;
document.addEventListener('DOMContentLoaded', () => {
    adminModule = new AdminModule();
}); 