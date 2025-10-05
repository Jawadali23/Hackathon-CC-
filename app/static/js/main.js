

document.addEventListener('DOMContentLoaded', function() {
    console.log('Harvest Calendar loaded successfully!');
    
    
    initializeNavigation();
    initializeAlerts();
    initializeTooltips();
    initializeForms();
    initializeAnimations();
    initializeSearchFeatures();
    initializeCalendarFeatures();
});


function initializeNavigation() {
    const navbar = document.querySelector('.navbar');
    
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
    }
}


function initializeAlerts() {
    
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert.parentNode) {
                alert.style.opacity = '0';
                setTimeout(function() {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 300);
            }
        }, 7000);
    });
}


function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}


function initializeForms() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(function(form) {
        
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Searching...';
                
                
                setTimeout(function() {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 5000);
            }
        });
        
        
        const searchInputs = form.querySelectorAll('input[type="text"], input[type="search"]');
        searchInputs.forEach(function(input) {
            input.addEventListener('input', Utils.debounce(function() {
                if (input.value.length > 2) {
                    performQuickSearch(input.value);
                }
            }, 300));
        });
    });
}


function initializeSearchFeatures() {
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        
        if (!searchInput.value) {
            searchInput.focus();
        }
        
        
        searchInput.addEventListener('input', Utils.debounce(function() {
            const query = searchInput.value.trim();
            if (query.length > 2) {
                showSearchSuggestions(query, searchInput);
            } else {
                hideSearchSuggestions();
            }
        }, 300));
        
        
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target)) {
                hideSearchSuggestions();
            }
        });
    }
}


function initializeCalendarFeatures() {
    
    const seasonCards = document.querySelectorAll('.card.border-success');
    seasonCards.forEach(function(card) {
        card.style.boxShadow = '0 0 20px rgba(40, 167, 69, 0.3)';
        card.classList.add('season-highlight');
    });
    
    
    const cropCards = document.querySelectorAll('.crop-card');
    const regionCards = document.querySelectorAll('.region-card');
    
    [...cropCards, ...regionCards].forEach(function(card) {
        card.addEventListener('click', function() {
            const link = card.querySelector('a');
            if (link) {
                link.click();
            }
        });
        
        
        card.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const link = card.querySelector('a');
                if (link) {
                    link.click();
                }
            }
        });
        
        
        card.setAttribute('tabindex', '0');
    });
    
    
    const calendarEntries = document.querySelectorAll('.card');
    calendarEntries.forEach(function(entry, index) {
        entry.style.animationDelay = `${index * 0.1}s`;
        entry.classList.add('fade-in');
    });
}


function initializeAnimations() {
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    
    const animatedElements = document.querySelectorAll('.card:not(.fade-in), .hero-section');
    animatedElements.forEach(function(el) {
        observer.observe(el);
    });
}


function showSearchSuggestions(query, inputElement) {
    
    let suggestionsDiv = document.getElementById('search-suggestions');
    if (!suggestionsDiv) {
        suggestionsDiv = document.createElement('div');
        suggestionsDiv.id = 'search-suggestions';
        suggestionsDiv.className = 'search-suggestions';
        inputElement.parentNode.appendChild(suggestionsDiv);
    }
    
    
    const mockSuggestions = [
        'Wheat', 'Rice', 'Corn', 'Potato', 'Bean', 'Lentil', 'Barley', 'Oats'
    ].filter(crop => crop.toLowerCase().includes(query.toLowerCase()));
    
    if (mockSuggestions.length > 0) {
        suggestionsDiv.innerHTML = mockSuggestions.map(suggestion => 
            `<div class="suggestion-item" onclick="selectSuggestion('${suggestion}')">${suggestion}</div>`
        ).join('');
        suggestionsDiv.style.display = 'block';
    } else {
        hideSearchSuggestions();
    }
}

function hideSearchSuggestions() {
    const suggestionsDiv = document.getElementById('search-suggestions');
    if (suggestionsDiv) {
        suggestionsDiv.style.display = 'none';
    }
}

function selectSuggestion(suggestion) {
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.value = suggestion;
        hideSearchSuggestions();
        
        const form = searchInput.closest('form');
        if (form) {
            form.submit();
        }
    }
}


function performQuickSearch(query) {
    fetch(`/quick-search?q=${encodeURIComponent(query)}&type=crop`)
        .then(response => response.json())
        .then(data => {
            
            console.log('Search results:', data);
        })
        .catch(error => {
            console.error('Search error:', error);
        });
}


function validateField(field) {
    const value = field.value.trim();
    let isValid = true;
    
    
    const existingFeedback = field.parentNode.querySelector('.invalid-feedback');
    if (existingFeedback) {
        existingFeedback.remove();
    }
    
    
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        showFieldError(field, 'This field is required.');
    }
    
    
    if (field.hasAttribute('minlength')) {
        const minLength = parseInt(field.getAttribute('minlength'));
        if (value.length < minLength) {
            isValid = false;
            showFieldError(field, `Please enter at least ${minLength} characters.`);
        }
    }
    
    
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }
    
    return isValid;
}


function showFieldError(field, message) {
    const feedback = document.createElement('div');
    feedback.className = 'invalid-feedback';
    feedback.textContent = message;
    field.parentNode.appendChild(feedback);
}


const Utils = {
    
    showLoading: function(element, text = 'Loading...') {
        element.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span>${text}`;
        element.disabled = true;
    },
    
    
    hideLoading: function(element, originalText) {
        element.innerHTML = originalText;
        element.disabled = false;
    },
    
    
    showNotification: function(message, type = 'success') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        
        setTimeout(function() {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    },
    
    
    formatDate: function(dateStr) {
        if (!dateStr) return 'N/A';
        
        try {
            
            if (dateStr.includes('/')) {
                const [day, month] = dateStr.split('/');
                const monthNames = [
                    'January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December'
                ];
                return `${parseInt(day)} ${monthNames[parseInt(month) - 1]}`;
            }
            return dateStr;
        } catch (error) {
            return dateStr;
        }
    },
    
    
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = function() {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    
    getCurrentMonth: function() {
        const monthNames = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        return monthNames[new Date().getMonth()];
    },
    
    
    isPlantingSeason: function(startDate, endDate) {
        const now = new Date();
        const currentMonth = now.getMonth() + 1;
        
        
        const startMonth = startDate ? parseInt(startDate.split('/')[1]) : null;
        const endMonth = endDate ? parseInt(endDate.split('/')[1]) : null;
        
        if (startMonth && endMonth) {
            if (startMonth <= endMonth) {
                return currentMonth >= startMonth && currentMonth <= endMonth;
            } else {
               
                return currentMonth >= startMonth || currentMonth <= endMonth;
            }
        }
        
        return false;
    }
};


const API = {
    
    getCropCalendar: async function(crop, region = null) {
        try {
            const params = new URLSearchParams({ crop });
            if (region) params.append('region', region);
            
            const response = await fetch(`/api/crop-calendar?${params}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('API Error:', error);
            return null;
        }
    },
    
    
    getStats: async function() {
        try {
            const response = await fetch('/api/stats');
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Stats API Error:', error);
            return null;
        }
    },
    
    
    quickSearch: async function(query, type = 'crop') {
        try {
            const params = new URLSearchParams({ q: query, type });
            const response = await fetch(`/quick-search?${params}`);
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Search API Error:', error);
            return null;
        }
    }
};


function printCalendar() {
    window.print();
}


window.HarvestCalendar = {
    Utils: Utils,
    API: API,
    printCalendar: printCalendar
};


const searchStyles = `
.search-suggestions {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 1px solid #ddd;
    border-radius: 0.375rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    max-height: 200px;
    overflow-y: auto;
    display: none;
}

.suggestion-item {
    padding: 0.5rem 1rem;
    cursor: pointer;
    border-bottom: 1px solid #f0f0f0;
}

.suggestion-item:hover {
    background-color: #f8f9fa;
}

.suggestion-item:last-child {
    border-bottom: none;
}
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = searchStyles;
document.head.appendChild(styleSheet);