window.addEventListener('load', () => {

    $('.faq-category').on('click', (e) => {
        $('.faq-category.selected').removeClass('selected');
        e.target.classList.add('selected');
        if(e.target.id == 'all') {
            $('.blog-article').css('display', '');
        } else {
            $('.blog-article').each((i, block) => {
                if(!block.classList.contains(e.target.id)) {
                    block.style.display = 'none';
                } else {
                    block.style.display = '';
                }
            })
        }
    })
})