
    function toggleImages() {
        for (let i = 0; i <= 4; i += 2) {
            var image1 = document.getElementById('image' + i);
            var image2 = document.getElementById('image' + (i + 1));
            if (image1.classList.contains('hidden')) {
                image1.classList.remove('hidden');
                image2.classList.add('hidden');
            } else {
                image1.classList.add('hidden');
                image2.classList.remove('hidden');
            }
        }
    }