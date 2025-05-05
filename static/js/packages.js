function toggleFlip(card) {
    const cardInner = card.querySelector('.card-inner');
    
    // Toggle flip: If the card is flipped, return to normal, else flip it
    if (cardInner.style.transform === 'rotateY(180deg)') {
        cardInner.style.transform = 'rotateY(0deg)';
    } else {
        cardInner.style.transform = 'rotateY(180deg)';
    }
}