window.addEventListener('load', () => {
    $('.m-header-menu-open').on('click', (e) => {
        let block = $('.m-header-menu-block');
        let close = $('.m-header-menu-close');
        let login = $('.header-login-button');
        let menu = $('.header-menu-block');

        block.css('display', 'block');
        close.css('display', 'block');
        login.css('display', 'flex');
        menu.css('display', 'flex');
        
        let time = 500;

        $('.m-header-menu-background').css('display', 'block');
        block.animate({
            'right': 0
        }, time)
        close.animate({
            'right': 15
        }, time)
        login.animate({
            'right': 83
        }, time)
        menu.animate({
            'right': 25
        }, time)
    })

    $('.close-menu').on('click', (e) => {
        let block = $('.m-header-menu-block');
        let close = $('.m-header-menu-close');
        let login = $('.header-login-button');
        let menu = $('.header-menu-block');
        
        $('.m-header-menu-background').css('display', '');

        let time = 500;
        block.animate({
            'right': -250
        }, time, () => {
            block.css('display', '');
        })
        close.animate({
            'right': -235
        }, time, () => {
            close.css('display', '');
        })
        login.animate({
            'right': -167
        }, time, () => {
            login.css('display', '');
        })
        menu.animate({
            'right': -225
        }, time, () => {
            menu.css('display', '');
        })
    })
})