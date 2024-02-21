window.addEventListener('load', () => {

    $('.index-question-block').each((i, block) => {
        let id = block.id.replace('faq-', '');
        block.style.height = $(`#question-${id}`).height() + 40 + 'px';
        $(`#answer-${id}`).css('height', 'auto');
    });

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
    
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    $('.index-question-top').on('mouseover', (e) => {
        let id = e.target.id.replace('question', 'cross');
        $(`#${id}`).css('filter', 'invert(1)');
    })

    $('.index-question-top').on('mouseout', (e) => {
        let id = e.target.id.replace('question', 'cross');
        $(`#${id}`).css('filter', '');
    })

    $('.index-question-top').on('click', (e) => {
        let id = e.target.id.replace('question-', '');
        if($(`#faq-${id}`).height() - 40 == $(`#question-${id}`).height()) {
            $(`#faq-${id}`).animate({
                'height': $(`#answer-${id}`).height() + $(`#question-${id}`).height() + 60 + 'px'
            }, 500)
        } else {
            $(`#faq-${id}`).animate({
                'height': $(`#question-${id}`).height() + 40 + 'px'
            }, 500)
        }  
    })

    window.addEventListener('resize', () => {

        $('.index-question-block').each((i, block) => {
            let id = block.id.replace('faq-', '');
            block.style.height = $(`#question-${id}`).height() + 40 + 'px';
            $(`#answer-${id}`).css('height', 'auto');
        });
    })
})