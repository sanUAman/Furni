document.addEventListener('DOMContentLoaded', function() {
    const mainImageBlock = document.getElementById('productMainImage');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const dataElement = document.getElementById('images-data');

    // Перевірка на існування елементів
    if (!mainImageBlock || !prevBtn || !nextBtn || !dataElement) {
        return; 
    }

    try {
        const images = JSON.parse(dataElement.textContent);
        
        // --- ДЕБАГ У КОНСОЛЬ БРАУЗЕРА ---
        console.log("[JS DEBUG] Знайдено масив картинок:", images);
        // ---------------------------------

        if (!images || images.length <= 1) {
            console.log("[JS DEBUG] Картинка лише одна або масив порожній. Гортання вимкнено.");
            prevBtn.style.display = 'none';
            nextBtn.style.display = 'none';
            return;
        }

        let currentIndex = 0;

        function updateImage(index) {
            console.log("[JS DEBUG] Перемикаємо на картинку №:", index, "URL:", images[index]);
            mainImageBlock.style.backgroundImage = `url('${images[index]}')`;
        }

        nextBtn.addEventListener('click', function() {
            currentIndex = (currentIndex + 1) % images.length;
            updateImage(currentIndex);
        });

        prevBtn.addEventListener('click', function() {
            currentIndex = (currentIndex - 1 + images.length) % images.length;
            updateImage(currentIndex);
        });
        
    } catch (e) {
        console.error("[JS DEBUG] Помилка парсингу JSON:", e);
    }
});