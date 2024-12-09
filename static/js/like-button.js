function renderLikeButton(auctionId, likeCount, isLiked) {
    const container = document.getElementById('auction-data');

    // Створення кнопки лайку
    const button = document.createElement('button');
    button.className = isLiked ? 'liked' : '';
    button.innerText = isLiked ? 'Dislike' : 'Like';
    button.setAttribute('data-auction-id', auctionId);

    // Створення елемента лічильника
    const likeCounter = document.createElement('span');
    likeCounter.id = 'likeCount';
    likeCounter.innerText = likeCount;

    // Додавання обробника подій
    button.addEventListener('click', function () {
        const initialLiked = button.classList.contains('liked');
        const newLikeCount = initialLiked ? likeCount - 1 : likeCount + 1;

        // Оновлення UI
        button.classList.toggle('liked');
        button.innerText = initialLiked ? 'Like' : 'Dislike';
        likeCounter.innerText = newLikeCount;

        // Відправка POST-запиту
        fetch(`https://auto-shop-3dd759c39636.herokuapp.com/auction/like-auction/${auctionId}/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ liked: !initialLiked }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                likeCounter.innerText = data.like_count;  // Оновлення лічильника після відповіді
            }
        })
        .catch(console.error);
    });

    // Додавання кнопки і лічильника в DOM
    container.appendChild(button);
    container.appendChild(likeCounter);
}
