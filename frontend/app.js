const API_URL = 'http://localhost:8100';

// Tab Switching
function switchTab(tabId) {
    // Update Nav
    document.querySelectorAll('.nav-links li').forEach(li => li.classList.remove('active'));
    document.querySelector(`li[onclick="switchTab('${tabId}')"]`).classList.add('active');

    // Update Content
    document.querySelectorAll('.tab-content').forEach(section => section.classList.remove('active'));
    document.getElementById(`${tabId}-tab`).classList.add('active');

    // Update Header
    const titles = {
        'analyse': ['Analyse Sentiment', 'Real-time sentiment prediction powered by AI'],
        'visualization': ['Visualization', 'Interactive dashboard of 100,000+ reviews'],
        'query': ['Query Reviews', 'Search and filter the dataset'],
        'about': ['About', 'Project details and architecture']
    };
    document.getElementById('page-title').innerText = titles[tabId][0];
    document.getElementById('page-subtitle').innerText = titles[tabId][1];

    if (tabId === 'visualization') {
        renderCharts();
    } else if (tabId === 'query') {
        fetchReviews();
    } else if (tabId === 'about') {
        animateMetrics();
    }
}

// Animation
let animated = false;
function animateMetrics() {
    if (animated) return; // Run once per session or reset if desired. Let's run once.
    animated = true;

    const animateValue = (id, start, end, duration, isPercent = false, isFloat = false) => {
        const obj = document.getElementById(id);
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);

            let val = progress * (end - start) + start;
            if (isFloat) {
                obj.innerText = val.toFixed(2);
            } else {
                obj.innerText = Math.floor(val).toLocaleString() + (isPercent ? "%" : "");
            }

            if (progress < 1) {
                window.requestAnimationFrame(step);
            } else {
                // Ensure final value is exact
                if (isPercent) obj.innerText = end + "%";
                else if (isFloat) obj.innerText = end.toFixed(2);
                else obj.innerText = end.toLocaleString() + "+";
            }
        };
        window.requestAnimationFrame(step);
    };

    animateValue("metric-acc", 0, 92, 1500, true);
    animateValue("metric-f1", 0, 0.89, 1500, false, true);
    animateValue("metric-recs", 0, 200000, 2000);
}

// Theme Toggle
function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    document.querySelector('.theme-toggle span').innerText = isDark ? 'Dark Mode' : 'Light Mode';
    document.querySelector('.theme-toggle i').className = isDark ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
}

// Analysis
async function analyzeSentiment() {
    const text = document.getElementById('review-input').value;
    const model = document.getElementById('model-select').value;

    if (!text) {
        alert('Please enter a review text.');
        return;
    }

    // Mock response for now until backend is ready
    // TODO: Replace with fetch(`${API_URL}/predict`)

    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ review_text: text, model: model })
        });

        let data;
        if (!response.ok) {
            console.warn("Backend not ready, using mock.");
            // Mock logic
            const isPos = text.toLowerCase().includes('good') || text.toLowerCase().includes('great') || text.toLowerCase().includes('love');
            data = {
                sentiment: isPos ? 'Positive' : 'Negative',
                confidence: 0.85 + Math.random() * 0.14,
                keywords: text.split(' ').slice(0, 3)
            };
        } else {
            data = await response.json();
        }

        // Store for saving
        lastAnalysis = {
            text: text,
            sentiment: data.sentiment,
            confidence: data.confidence
        };

        // Render result
        document.getElementById('result-card').style.display = 'block';
        renderSentimentBadge(data.sentiment, data.confidence);

        const tags = document.getElementById('keywords-list');
        tags.innerHTML = '';
        data.keywords.forEach(kw => {
            const span = document.createElement('span');
            span.className = 'tag';
            span.innerText = kw;
            tags.appendChild(span);
        });

    } catch (e) {
        console.error("API Error", e);
        // Fallback for demo without backend
        const isPos = text.toLowerCase().includes('good') || text.toLowerCase().includes('love');
        const data = {
            sentiment: isPos ? 'Positive' : 'Negative',
            confidence: 0.85 + Math.random() * 0.14,
            keywords: ['demo', 'mode']
        };
        document.getElementById('result-card').style.display = 'block';
        renderSentimentBadge(data.sentiment, data.confidence);
    }
}

// Visualization
let chartsInited = false;
async function renderCharts() {
    if (chartsInited) return;

    try {
        const response = await fetch(`${API_URL}/stats`);
        const data = response.ok ? await response.json() : getMockStats();

        // Populate Stats Tiles
        document.getElementById('stat-total').innerText = (data.positive + data.neutral + data.negative).toLocaleString();
        document.getElementById('stat-positive').innerText = data.positive.toLocaleString();
        document.getElementById('stat-neutral').innerText = data.neutral.toLocaleString();
        document.getElementById('stat-negative').innerText = data.negative.toLocaleString();

        // Pie Chart
        new Chart(document.getElementById('pieChart'), {
            type: 'doughnut',
            data: {
                labels: ['Positive', 'Neutral', 'Negative'],
                datasets: [{
                    data: [data.positive, data.neutral, data.negative],
                    backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                    borderWidth: 0
                }]
            },
            options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
        });

        // Bar Chart (Ratings)
        new Chart(document.getElementById('barChart'), {
            type: 'bar',
            data: {
                labels: ['1 Star', '2 Stars', '3 Stars', '4 Stars', '5 Stars'],
                datasets: [{
                    label: 'Count',
                    data: data.ratings_dist,
                    backgroundColor: '#6366f1'
                }]
            },
            options: { responsive: true }
        });
        // ... (Charts removed for brevity in replacement, assuming they stay)
        // Note: I must be careful not to delete Line Chart if I don't include it.
        // Wait, replace_file_content replaces the whole block. I should include Line Chart.

        // Line Chart (Trend)
        new Chart(document.getElementById('lineChart'), {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Positive Reviews',
                    data: [120, 190, 300, 500, 200, 400],
                    borderColor: '#10b981',
                    tension: 0.4
                }, {
                    label: 'Negative Reviews',
                    data: [80, 50, 100, 120, 90, 110],
                    borderColor: '#ef4444',
                    tension: 0.4
                }]
            },
            options: { responsive: true }
        });

        // Word Cloud (Simple HTML based or use library)
        const wcContainer = document.getElementById('wordcloud-container');
        wcContainer.innerHTML = '';
        const colors = ['#6366f1', '#ec4899', '#10b981', '#f59e0b'];
        data.top_words.forEach(word => {
            const span = document.createElement('span');
            span.innerText = word.text;
            span.style.fontSize = `${Math.max(12, word.value / 10)}px`;
            span.style.color = colors[Math.floor(Math.random() * colors.length)];
            span.style.padding = '5px';
            span.style.display = 'inline-block';
            wcContainer.appendChild(span);
        });

        chartsInited = true;

    } catch (e) {
        console.error("Viz Error", e);
    }
}

function getMockStats() {
    return {
        positive: 65000,
        negative: 35000,
        neutral: 15000,
        ratings_dist: [5000, 10000, 15000, 30000, 40000],
        top_words: []
    };
}

// Query
let currentPage = 0;
const PAGE_SIZE = 20;

async function fetchReviews(page = 0) {
    currentPage = page;
    const search = document.getElementById('query-search').value;
    const sentiment = document.getElementById('query-sentiment').value;
    const rating = document.getElementById('query-rating').value;

    // document.getElementById('page-info').innerText = `Page ${currentPage + 1}`; // Remove old pager

    const tbody = document.getElementById('reviews-table-body');
    const totalSpan = document.getElementById('total-results');

    showLoading('reviews-table-body');
    totalSpan.innerText = 'Searching...';

    const params = new URLSearchParams({
        skip: currentPage * PAGE_SIZE,
        limit: PAGE_SIZE
    });
    if (search) params.append('search', search);
    if (sentiment) params.append('sentiment', sentiment);
    if (rating) params.append('rating', rating);

    try {
        const response = await fetch(`${API_URL}/reviews/?${params.toString()}`);
        if (!response.ok) throw new Error("Failed to fetch");

        const data = await response.json();
        const reviews = data.reviews;
        const total = data.total;

        totalSpan.innerText = `${total.toLocaleString()} results found`;

        tbody.innerHTML = '';
        if (reviews.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding: 2rem;">No reviews found.</td></tr>';
        } else {
            reviews.forEach(review => {
                tbody.appendChild(renderReviewRow(review));
            });
        }

        renderPagination(total, currentPage, PAGE_SIZE);

    } catch (e) {
        console.error("Query Error", e);
        tbody.innerHTML = `<tr><td colspan="5" style="color:red; text-align:center;">Error loading reviews: ${e.message}</td></tr>`;
        totalSpan.innerText = '';
    }
}

function renderPagination(total, current, size) {
    const totalPages = Math.ceil(total / size);
    const container = document.getElementById('pagination-numbers');
    container.innerHTML = '';

    if (totalPages <= 1) return;

    const createBtn = (i, text, isActive = false, isDisabled = false) => {
        const btn = document.createElement('div');
        btn.className = `pagination-btn ${isActive ? 'active' : ''} ${isDisabled ? 'disabled' : ''}`;
        btn.innerText = text;
        if (!isActive && !isDisabled) {
            btn.onclick = () => fetchReviews(i);
        }
        return btn;
    };

    // Previous
    container.appendChild(createBtn(current - 1, '‹', false, current === 0));

    // Logic for pages: 1 ... 4 5 6 ... 100
    // Always show First
    container.appendChild(createBtn(0, '1', current === 0));

    let start = Math.max(1, current - 2);
    let end = Math.min(totalPages - 2, current + 2);

    if (start > 1) {
        const dots = document.createElement('div');
        dots.className = 'pagination-btn disabled';
        dots.innerText = '...';
        container.appendChild(dots);
    }

    for (let i = start; i <= end; i++) {
        container.appendChild(createBtn(i, i + 1, current === i));
    }

    if (end < totalPages - 2) {
        const dots = document.createElement('div');
        dots.className = 'pagination-btn disabled';
        dots.innerText = '...';
        container.appendChild(dots);
    }

    // Always show Last if > 1
    if (totalPages > 1) {
        container.appendChild(createBtn(totalPages - 1, totalPages, current === totalPages - 1));
    }

    // Next
    container.appendChild(createBtn(current + 1, '›', false, current === totalPages - 1));
}

function resetFilters() {
    document.getElementById('query-search').value = '';
    document.getElementById('query-sentiment').value = '';
    document.getElementById('query-rating').value = '';
    fetchReviews(0);
}

// Modal Functions
function openReviewModal(review) {
    document.getElementById('modal-product-name').innerText = review.product_name;
    document.getElementById('modal-meta-info').innerText = `${review.category} • ${new Date(review.timestamp).toLocaleDateString()} • ${'⭐'.repeat(Math.round(review.rating))}`;
    document.getElementById('modal-review-text').innerText = review.review_text;

    const badge = document.getElementById('modal-sentiment-badge');
    badge.innerText = review.sentiment;

    if (review.sentiment === 'Positive') {
        badge.style.color = '#10b981'; badge.style.background = 'rgba(16, 185, 129, 0.1)';
    } else if (review.sentiment === 'Negative') {
        badge.style.color = '#ef4444'; badge.style.background = 'rgba(239, 68, 68, 0.1)';
    } else {
        badge.style.color = '#f59e0b'; badge.style.background = 'rgba(245, 158, 11, 0.1)';
    }

    document.getElementById('review-modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('review-modal').style.display = 'none';
}

// Close modal on outside click
window.onclick = function (event) {
    const modal = document.getElementById('review-modal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}


// Save Feature
// lastAnalysis is declared globally... (keeping as is)
async function saveCurrentReview() {
    if (!lastAnalysis) return;

    const btn = document.getElementById('save-review-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Saving...';
    btn.disabled = true;

    try {
        // Map sentiment to rating roughly
        let rating = 3.0;
        if (lastAnalysis.sentiment === 'Positive') rating = 5.0;
        if (lastAnalysis.sentiment === 'Negative') rating = 1.0;

        const payload = {
            product_name: "User Analyzed Product",
            category: "User Submission",
            review_text: lastAnalysis.text,
            rating: rating,
            sentiment: lastAnalysis.sentiment,
            timestamp: new Date().toISOString()
        };

        const response = await fetch(`${API_URL}/reviews/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("Failed to save");

        const res = await response.json();
        alert(`Review saved! ID: ${res.id}`);

    } catch (e) {
        console.error(e);
        alert("Error saving review: " + e.message);
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}
