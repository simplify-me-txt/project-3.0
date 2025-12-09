function renderSentimentBadge(sentiment, confidence) {
    const badge = document.getElementById('sentiment-badge');
    const fill = document.getElementById('confidence-fill');
    const score = document.getElementById('confidence-score');

    badge.innerText = sentiment.toUpperCase();
    badge.className = 'sentiment-badge'; // Reset

    // Set color based on sentiment
    if (sentiment.toLowerCase() === 'positive') {
        badge.style.color = '#10b981';
        badge.style.background = 'rgba(16, 185, 129, 0.1)';
        fill.style.background = 'linear-gradient(90deg, #10b981, #34d399)';
    } else if (sentiment.toLowerCase() === 'negative') {
        badge.style.color = '#ef4444';
        badge.style.background = 'rgba(239, 68, 68, 0.1)';
        fill.style.background = 'linear-gradient(90deg, #ef4444, #f87171)';
    } else {
        // Neutral
        badge.style.color = '#f59e0b';
        badge.style.background = 'rgba(245, 158, 11, 0.1)';
        fill.style.background = 'linear-gradient(90deg, #f59e0b, #fbbf24)';
    }

    // Animate confidence
    setTimeout(() => {
        fill.style.width = `${confidence * 100}%`;
    }, 100);

    score.innerText = `${Math.round(confidence * 100)}%`;
}

function renderReviewRow(review, index) {
    const tr = document.createElement('tr');
    tr.className = 'review-row-clickable';
    tr.onclick = () => openReviewModal(review); // Direct function reference if review is object
    // Wait, tr.onclick = () => ... works if we attach the listener in JS, 
    // but `tbody.innerHTML += ...` converts to string.
    // If we use `tbody.appendChild(tr)`, then `tr.onclick` works perfectly with the object closure!
    // My app.js uses `tbody.appendChild(renderReviewRow(review))`. So this is perfect.

    let color = '#f59e0b'; // Neutral default
    if (review.sentiment === 'Positive') color = '#10b981';
    if (review.sentiment === 'Negative') color = '#ef4444';

    tr.innerHTML = `
        <td>
            <div style="font-weight: 500">${review.product_name}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted)">${review.category}</div>
        </td>
        <td>
            <div style="font-size: 0.9rem; color: var(--text-muted); cursor: pointer;" title="Click to read full review">
                ${review.review_text.substring(0, 80)}${review.review_text.length > 80 ? '...' : ''}
            </div>
        </td>
        <td>${'⭐'.repeat(Math.round(review.rating))}</td>
        <td style="font-weight: 600; color: ${color}">
            ${review.sentiment}
        </td>
        <td style="color: var(--text-muted); font-size: 0.9rem;">
            ${new Date(review.timestamp).toLocaleDateString()}
        </td>
    `;
    return tr;
}

function showLoading(elementId) {
    const el = document.getElementById(elementId);
    if (el) {
        el.innerHTML = '<div style="text-align:center; padding: 2rem;"><i class="fa-solid fa-spinner fa-spin fa-2x"></i></div>';
    }
}
