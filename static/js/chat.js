window.addEventListener('load', () => {

    let currentSamples = 'public';

    let requestLock = false;
    let requestTotal = 0;
    let requestQuantity = {
        "GPT35": 0,
        "GPT4": 0,
        "VS": 0,
        "SD": 0,
        "MJ": 0
    }

    let sampleOn = false;
    let sampleVars = {};

    const classData = {
        'public': 'like',
        'private': 'delete',
        'favorites': 'unlike'
    }

    const svgData = {
        'public': '<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 1024 1024" height="16" width="16" xmlns="http://www.w3.org/2000/svg"><path d="M923 283.6a260.04 260.04 0 0 0-56.9-82.8 264.4 264.4 0 0 0-84-55.5A265.34 265.34 0 0 0 679.7 125c-49.3 0-97.4 13.5-139.2 39-10 6.1-19.5 12.8-28.5 20.1-9-7.3-18.5-14-28.5-20.1-41.8-25.5-89.9-39-139.2-39-35.5 0-69.9 6.8-102.4 20.3-31.4 13-59.7 31.7-84 55.5a258.44 258.44 0 0 0-56.9 82.8c-13.9 32.3-21 66.6-21 101.9 0 33.3 6.8 68 20.3 103.3 11.3 29.5 27.5 60.1 48.2 91 32.8 48.9 77.9 99.9 133.9 151.6 92.8 85.7 184.7 144.9 188.6 147.3l23.7 15.2c10.5 6.7 24 6.7 34.5 0l23.7-15.2c3.9-2.5 95.7-61.6 188.6-147.3 56-51.7 101.1-102.7 133.9-151.6 20.7-30.9 37-61.5 48.2-91 13.5-35.3 20.3-70 20.3-103.3.1-35.3-7-69.6-20.9-101.9zM512 814.8S156 586.7 156 385.5C156 283.6 240.3 201 344.3 201c73.1 0 136.5 40.8 167.7 100.4C543.2 241.8 606.6 201 679.7 201c104 0 188.3 82.6 188.3 184.5 0 201.2-356 429.3-356 429.3z"></path></svg>',
        'private': '<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 1024 1024" fill-rule="evenodd" height="16" width="16" xmlns="http://www.w3.org/2000/svg"><path d="M799.855 166.312c.023.007.043.018.084.059l57.69 57.69c.041.041.052.06.059.084a.118.118 0 0 1 0 .069c-.007.023-.018.042-.059.083L569.926 512l287.703 287.703c.041.04.052.06.059.083a.118.118 0 0 1 0 .07c-.007.022-.018.042-.059.083l-57.69 57.69c-.041.041-.06.052-.084.059a.118.118 0 0 1-.069 0c-.023-.007-.042-.018-.083-.059L512 569.926 224.297 857.629c-.04.041-.06.052-.083.059a.118.118 0 0 1-.07 0c-.022-.007-.042-.018-.083-.059l-57.69-57.69c-.041-.041-.052-.06-.059-.084a.118.118 0 0 1 0-.069c.007-.023.018-.042.059-.083L454.073 512 166.371 224.297c-.041-.04-.052-.06-.059-.083a.118.118 0 0 1 0-.07c.007-.022.018-.042.059-.083l57.69-57.69c.041-.041.06-.052.084-.059a.118.118 0 0 1 .069 0c.023.007.042.018.083.059L512 454.073l287.703-287.702c.04-.041.06-.052.083-.059a.118.118 0 0 1 .07 0Z"></path></svg>',
        'favorites': '<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 1024 1024" height="16" width="16" xmlns="http://www.w3.org/2000/svg"><path d="M923 283.6a260.04 260.04 0 0 0-56.9-82.8 264.4 264.4 0 0 0-84-55.5A265.34 265.34 0 0 0 679.7 125c-49.3 0-97.4 13.5-139.2 39-10 6.1-19.5 12.8-28.5 20.1-9-7.3-18.5-14-28.5-20.1-41.8-25.5-89.9-39-139.2-39-35.5 0-69.9 6.8-102.4 20.3-31.4 13-59.7 31.7-84 55.5a258.44 258.44 0 0 0-56.9 82.8c-13.9 32.3-21 66.6-21 101.9 0 33.3 6.8 68 20.3 103.3 11.3 29.5 27.5 60.1 48.2 91 32.8 48.9 77.9 99.9 133.9 151.6 92.8 85.7 184.7 144.9 188.6 147.3l23.7 15.2c10.5 6.7 24 6.7 34.5 0l23.7-15.2c3.9-2.5 95.7-61.6 188.6-147.3 56-51.7 101.1-102.7 133.9-151.6 20.7-30.9 37-61.5 48.2-91 13.5-35.3 20.3-70 20.3-103.3.1-35.3-7-69.6-20.9-101.9zM512 814.8S156 586.7 156 385.5C156 283.6 240.3 201 344.3 201c73.1 0 136.5 40.8 167.7 100.4C543.2 241.8 606.6 201 679.7 201c104 0 188.3 82.6 188.3 184.5 0 201.2-356 429.3-356 429.3z"></path></svg>'
    }

    let validatedInputs = {
        'name': false,
        'text': false,
        'var-text': true,
        'var-text2': true,
        'var-text3': true
    }

    let validatedInputsCount = 3;

    if(('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0)) {
        $('.chat-samples-help-block').addClass('mobile');
        $('.help-bg').addClass('mobile');
    }

    $('.chat-samples-public .chat-sample-like-block').each((i, block) => {
        if(favoritesPks.includes(parseInt(block.classList[1].replace('sample-', '')))) {
            block.className = `chat-sample-unlike-block ${block.classList[1]}`;
        }
    })

    $('.chat-clickable').on('click', (e) => {
        $('.chat-background-content').css('display', '');
        $('.chat-background').css('display', 'flex');
        $(`#${e.target.classList[2].replace('clickable', 'bg')}`).css('display', 'flex')
    });

    $('.chat-payment-clickable').on('click', (e) => {
        let subject = e.target.classList[2];
        if(subject == 'payment-tariffs') {
            let id = e.target.id.search('current') != -1 ? e.target.id.replace('current-tariff-', '') : e.target.id.replace('tariff-', '');
            $('.chat-payment-tariffs-name').html($(`#tariff-name-${id}`).html());
            $('.chat-payment-tariffs-submit').attr('id', 'payment-' + e.target.id);
        } else if(subject == 'payment-requests') {
            $('.chat-payment-requests-balance').html($('.chat-bg-request-total').html());
        }
        $('.chat-payment-content').css('display', '');
        $('.chat-payment-bg').css('display', 'flex');
        $(`#${subject}`).css('display', 'flex');
    });

    $('.chat-bg-close').on('click', () => {
        $('.chat-background-content').css('display', '');
        $('.chat-background').css('display', '');
    });

    $('.chat-payment-close').on('click', () => {
        $('.chat-payment-tariffs-name').html('');
        $('.chat-payment-requests-balance').html('');
        $('.chat-payment-tariffs-submit').removeAttr('id');
        $('.chat-payment-content').css('display', '');
        $('.chat-payment-bg').css('display', '');
    });

    $('.chat-payment-bg').on('click', (e) => {
        if(e.target.classList.contains('chat-payment-bg')) {
            $('.chat-payment-tariffs-name').html('');
            $('.chat-payment-requests-balance').html('');
            $('.chat-payment-tariffs-submit').removeAttr('id');
            $('.chat-payment-content').css('display', '');
            $('.chat-payment-bg').css('display', '');
        }
    })

    $('.chat-background').on('click', (e) => {
        if(e.target.classList.contains('chat-background-clickable')) {
            $('.chat-background-content').css('display', '');
            $('.chat-background').css('display', '');
        }
    });

    function placeholderFocus(e) {
        let target;
        if(e.target.getAttribute("class").search('input') == -1) {
            target = e.target;
        } else {
            target = e.target.parentNode;
        }
        target.querySelector('span').classList.add('active');
    }

    function placeholderFocusOut(e) {
        let target;
        if(e.target.getAttribute("class").search('input') == -1) {
            target = e.target;
        } else {
            target = e.target.parentNode;
        }
        if($(`#${target.id.replace('block', 'input')}`).val().length == 0) {
            target.querySelector('span').classList.remove('active');
        }
    }

    $('.chat-auth-input-block').on('click', (e) => {
        placeholderFocus(e);
    })

    $('.chat-auth-input').on('focus', (e) => {
        placeholderFocus(e);
    })

    $('.chat-auth-input-block').on('focusout', (e) => {
        placeholderFocusOut(e);
    })

    $(document).on('click', '.chat-chat-variable-block', (e) => {
        placeholderFocus(e);
    })

    $(document).on('focusout', '.chat-chat-variable-block', (e) => {
        placeholderFocusOut(e);
    })

    $('.chat-auth-input').on('focus', (e) => {
        e.target.parentNode.classList.add('active');
    })

    $('.chat-auth-input').on('blur', (e) => {
        e.target.parentNode.classList.remove('active');
    })

    function hideTags() {
        $(`.chat-samples-${currentSamples} .chat-sample-tags`).each((i, block) => {
            let moreBlock = block.querySelector('.chat-sample-tag-more');
            let helpBlock = document.querySelector(`.help-${currentSamples}-${block.parentNode.parentNode.id}`);
            let width = block.offsetWidth - 36;
            let currentWidth = 0;
            let toHide = [];
            let toReveal = [];
            for(let child of block.querySelectorAll('.chat-sample-tag')) {
                let childWidth = child.offsetWidth + 5;
                if(currentWidth + childWidth >= width) {
                    toHide.push([child.classList[1], child.innerHTML]);
                    child.remove();
                    currentWidth -= childWidth;
                } else {
                    currentWidth += childWidth;  
                }
            }
            helpBlock.style.visibility = 'hidden';
            helpBlock.style.display = 'flex';
            for(let child of helpBlock.querySelectorAll('.chat-sample-tag')) {
                let childWidth = child.offsetWidth + 5;
                if(currentWidth + childWidth < width) {
                    currentWidth += childWidth;
                    child.remove();
                    toReveal.push([child.classList[1], child.innerHTML]);
                }
            }
            helpBlock.style.display = '';
            helpBlock.style.visibility = '';

            for(let child of toReveal) {
                let childHtml = document.createElement('div');
                childHtml.setAttribute('class', `chat-sample-tag ${child[0]}`);
                childHtml.innerHTML = child[1];
                moreBlock.before(childHtml);
            }
            if(toHide.length > 0) {
                moreBlock.style.display = 'flex';
                for(let child of toHide) {
                    let childHtml = document.createElement('div');
                    childHtml.setAttribute('class', `chat-sample-tag ${child[0]} hidden`);
                    childHtml.innerHTML = child[1];
                    helpBlock.append(childHtml);
                }
                block.querySelector('.chat-sample-tag-more > span').innerHTML = '+' + helpBlock.children.length;
            }
            if(helpBlock.children.length == 0) {
                moreBlock.style.display = '';
            }
        })
    }

    $('#open-samples:not(.blocked)').on('click', () => {
        $('.chat-samples-container').css('display', 'flex');
        $('.chat-chat-block').css('display', 'none');
        $('.chat-samples-public').css('display', 'flex');
        $('#chat-samples-public').addClass('selected');
        hideTags();
    })

    $(document).on('click', '.chat-samples-menu-subblock:not(.selected)', (e) => {
        if(e.target.id == 'chat-samples-close') {
            $('.chat-samples-container').css('display', '');
            $('.chat-chat-block').css('display', '');
            $('.chat-samples-content').css('display', '');
            $('.chat-samples-menu-subblock').removeClass('selected');
        } else {
            if(e.target.id == 'chat-samples-create') {
                $('.chat-samples-content-top').css('display', 'none');
            } else {
                $('.chat-samples-content-top').css('display', '');
                currentSamples = e.target.id.replace('chat-samples-', '');
            }
            $('.chat-sample-wrapper').css('display', '');
            $('.chat-samples-content').css('display', '');
            $('.chat-samples-menu-subblock').removeClass('selected');
            e.target.classList.add('selected');
            $(`.${e.target.id}`).css('display', 'flex');
            hideTags();
        }
    })

    $(document).on('click', '.chat-samples-button', () => {
        $('#chat-samples-create').click();
    })

    $('#open-categories').on('click', (e) => {
        if($('.chat-samples-categories').css('display') == 'none') {
            $('.chat-samples-categories').css('display', 'flex');
        }
        e.stopPropagation();
    })

    $(document).on('click', (e) => {
        if(!e.target.classList.contains('chat-samples-categories') && e.target.id != 'open-categories') {
            $('.chat-samples-categories').css('display', 'none');
        }
    })

    $(document).on('mouseover', '.help-trigger', (e) => {
        if(!('ontouchstart' in window) && !(navigator.maxTouchPoints > 0) && !(navigator.msMaxTouchPoints > 0)) {
            let target = $(`#${e.target.id}`);
            let position = target.offset();
            let helpBlock = $(`.${e.target.id}`);
            let diff = e.target.id.search('sample') != -1 ? -5 : 15;
            helpBlock.css({'display': 'block', 'top': position.top - helpBlock.height() - diff, 'left': position.left + (target.outerWidth() / 2) - (helpBlock.width() / 2)});
            $('.chat-samples-help-bottom').css({'display': 'block', 'top': position.top - diff + 1, 'left': position.left + (target.outerWidth() / 2) - 5});
        }
    })

    $(document).on('mouseout', '.help-trigger', (e) => {
        $('.chat-samples-help-block').css('display', '');
        $('.chat-samples-help-bottom').css('display', '');
    })

    $(document).on('click', '.help-trigger', (e) => {
        if(('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0)) {
            $(`.${e.target.id}`).css('display', 'block');
            $('.help-bg').css('display', 'block');
        }
    })

    $(document).on('click', '.help-bg', (e) => {
        $('.chat-samples-help-block').css('display', '');
        e.target.style.display = '';
    })

    $(document).on('click', '.chat-sample-tag-more', (e) => {
        e.stopPropagation();
        let target = $(`#${e.target.id}`);
        let position = target.offset();
        let helpBlock = $(`.${e.target.id}`);
        let diff = 15;
        helpBlock.css({'display': 'flex', 'top': position.top - helpBlock.height() - diff, 'left': position.left + (target.outerWidth() / 2) - (helpBlock.width() / 2)});
        $('.chat-samples-help-bottom').css({'display': 'block', 'top': position.top - diff + 1, 'left': position.left + (target.outerWidth() / 2) - 5});
        $('.chat-sample-more-bg').css('display', 'block');
    })

    $(document).on('click', '.chat-sample-more-bg', (e) => {
        e.target.style.display = '';
        $('.chat-samples-help-block').css('display', '');
        $('.chat-samples-help-bottom').css('display', '');
    })

    $(document).on('mouseover', '.blocked', (e) => {
        if(!('ontouchstart' in window) && !(navigator.maxTouchPoints > 0) && !(navigator.msMaxTouchPoints > 0)) {
            let target = $(`#${e.target.id}`);
            let position = target.offset();
            let helpBlock = $('.help-5');
            let diff = 10;
            let top = position.top + (target.outerHeight() / 2);
            if(window.innerWidth < position.left + target.outerWidth() + helpBlock.width() + diff) {
                helpBlock.css({'display': 'block', 'top': top - (helpBlock.outerHeight() / 2), 'left': position.left - helpBlock.width() - diff - 10});
                $('.chat-samples-help-right').css({'display': 'block', 'top': top - 5, 'left': position.left - 9 - diff});
            } else {
                helpBlock.css({'display': 'block', 'top': top - (helpBlock.outerHeight() / 2), 'left': position.left + target.outerWidth() + diff + 5});
                $('.chat-samples-help-left').css({'display': 'block', 'top': top - 5, 'left': position.left + target.outerWidth() + diff});
            }
        }
    })

    $(document).on('mouseout', '.blocked', () => {
        $('.help-5').css('display', '');
        $('.chat-samples-help-left').css('display', '');
        $('.chat-samples-help-right').css('display', '');
    })

    $(document).on('click', '.blocked', (e) => {
        if(('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0)) {
            $('.help-5').css('display', 'block');
            $('.help-bg').css('display', 'block');
        }
    })

    function getSampleHTML(sample, mode) {
        $(`.help-${currentSamples}-sample-${sample.pk}`).html('');
        htmlString = `<div class="chat-sample-wrapper">
                        <div class="chat-sample-block" id="sample-${sample.pk}">
                            <div class="chat-sample-top">
                                <div class="chat-sample-tags">`;
        for(let catPk of sample.fields.categories) {
            htmlString += `<div class="chat-sample-tag category-${catPk}">${categoriesJs[catPk]}</div>`;
        }
        htmlString += `<div class="chat-sample-tag-more" id="help-${currentSamples}-sample-${sample.pk}">
                            <span></span>
                        </div>
                    </div>
                        <div class="chat-sample-${classData[mode]}-block sample-${sample.pk}">
                            ${svgData[mode]}
                        </div>
                    </div>
                    <h2 class="chat-sample-name">${sample.fields.name}</h2>
                    <p class="chat-sample-description">${sample.fields.description}</p>
                </div>
            </div>`;
        return htmlString;
    }

    function setSamples(pk) {
        let htmlString = '';
        for(let sample of samplesData[currentSamples]) {
            if(pk == 'all' || sample.fields.categories.includes(pk)) {
                let mode = currentSamples == 'public' && favoritesPks.includes(sample.pk) ? 'favorites' : currentSamples;
                htmlString += getSampleHTML(sample, mode);
            }
        }
        if(htmlString.length > 0) {
            $(`.chat-samples-${currentSamples} .chat-samples-block`).html(htmlString);
            $(`.chat-samples-${currentSamples} .chat-samples-nothing`).css('display', '');
        } else {
            $(`.chat-samples-${currentSamples} .chat-samples-nothing`).css('display', 'block');
        }
        hideTags();
    }

    $('.chat-samples-category').on('click', (e) => {
        let pk = e.target.classList[1].replace('category-', '');
        pk = pk == 'all' ? pk : parseInt(pk);
        setSamples(pk);
        $('.chat-samples-current-category').html(e.target.innerHTML);
    })

    $(document).on('click', '.chat-sample-tag', (e) => {
        e.stopPropagation();
        $('.chat-samples-help-bottom').css('display', '');
        $('.chat-samples-help-block').css('display', '');
        let pk = parseInt(e.target.classList[1].replace('category-', ''));
        setSamples(pk);
        $('.chat-samples-current-category').html(e.target.innerHTML);
    })

    $('.chat-samples-search-block').on('click', (e) => {
        if($('.chat-samples-search').css('display') == 'none') {
            $('.chat-samples-categories-block').css('display', 'none');
            $('.chat-samples-search').css('display', 'block');
            $('.chat-samples-search-hide').css('display', 'flex');
            $('.chat-samples-search-block').addClass('visible');
        }
    })

    $('.chat-samples-search-hide').on('click', (e) => {
        e.stopPropagation();
        $('.chat-samples-categories-block').css('display', '');
        $('.chat-samples-search').css('display', '');
        $('.chat-samples-search-hide').css('display', '');
        $('.chat-samples-search-block').removeClass('visible');
    })

    $('.chat-samples-search').on('input', (e) => {
        let value = e.target.value;
        let htmlString = '';
        for(let sample of samplesData[currentSamples]) {
            if(sample.fields.name.toLowerCase().search(value.toLowerCase()) != -1 || sample.fields.description.toLowerCase().search(value.toLowerCase()) != -1) {
                let mode = currentSamples == 'public' && favoritesPks.includes(sample.pk) ? 'favorites' : currentSamples;
                htmlString += getSampleHTML(sample, mode);
            }
        }
        if(htmlString.length > 0) {
            $(`.chat-samples-${currentSamples} .chat-samples-block`).html(htmlString);
            $(`.chat-samples-${currentSamples} .chat-samples-nothing`).css('display', '');
        } else {
            $(`.chat-samples-${currentSamples} .chat-samples-block`).html(htmlString);
            $(`.chat-samples-${currentSamples} .chat-samples-nothing`).css('display', 'block');
        }
        hideTags();
    })

    $(document).on('click', '.chat-sample-like-block', (e) => {
        e.stopPropagation();
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let pk = e.target.classList[1].replace('sample-', '');
        $.ajax({
            method: "post",
            url: "/chat/like_sample/",
            data: {csrfmiddlewaretoken: token, pk: pk},
            success: (data) => {
                if(data['result'] == 'ok') {
                    e.target.className = `chat-sample-unlike-block sample-${pk}`;
                    $('.chat-samples-favorites .chat-samples-block').append(getSampleHTML(data['sample'], 'favorites'));
                    samplesData['favorites'].push(data['sample']);
                    if(samplesData['favorites'].length == 1) {
                        $('.chat-samples-favorites .chat-samples-empty').css('display', 'none');
                    }
                }
            },
            error: (data) => {
            }
        });
    })

    $(document).on('click', '.chat-sample-delete-block', (e) => {
        e.stopPropagation();
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let pk = parseInt(e.target.classList[1].replace('sample-', ''));
        $.ajax({
            method: "post",
            url: "/chat/delete_sample/",
            data: {csrfmiddlewaretoken: token, pk: pk},
            success: (data) => {
                if(data['result'] == 'ok') {
                    e.target.parentNode.parentNode.parentNode.remove();
                    samplesData['private'] = samplesData['private'].filter((sample) => {
                        return sample.pk != pk;
                    })
                    if(samplesData['private'].length == 0) {
                        $('.chat-samples-private .chat-samples-empty').css('display', '');
                        $('.chat-samples-private .chat-samples-button').css('display', '');
                    }
                }
            },
            error: (data) => {
            }
        });
    })

    $(document).on('click', '.chat-sample-unlike-block', (e) => {
        e.stopPropagation();
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let pk = parseInt(e.target.classList[1].replace('sample-', ''));
        $.ajax({
            method: "post",
            url: "/chat/unlike_sample/",
            data: {csrfmiddlewaretoken: token, pk: pk},
            success: (data) => {
                if(data['result'] == 'ok') {
                    $(`.chat-samples-public .chat-sample-unlike-block.sample-${pk}`).attr('class', `chat-sample-like-block sample-${pk}`)
                    $(`.chat-samples-favorites .chat-sample-unlike-block.sample-${pk}`).parent().parent().parent().remove()
                    samplesData['favorites'] = samplesData['favorites'].filter((sample) => {
                        return sample.pk != pk;
                    })
                    if(samplesData['favorites'].length == 0) {
                        $('.chat-samples-favorites .chat-samples-empty').css('display', '');
                    }
                    favoritesPks = favoritesPks.filter((fav) => {
                        return fav != pk;
                    })
                }
            },
            error: (data) => {
            }
        });
    })

    $('.chat-samples-input').on('input', (e) => {
        let type = e.target.classList[1];
        if(type != 'description') {
            if(type == 'variable') {
                type = e.target.parentNode.id;
            }

            if(e.target.value.length > 0 && validatedInputs[type] == false) {
                $(`#warning-${type}`).css('display', 'none');
                validatedInputsCount += 1;
                validatedInputs[type] = true;
                if(validatedInputsCount == 5) {
                    $('.chat-samples-create-button').addClass('active');
                }
            } else if(e.target.value.length == 0 && validatedInputs[type] == true) {
                $(`#warning-${type}`).css('display', '');
                validatedInputsCount -= 1;
                validatedInputs[type] = false;
                if(validatedInputsCount == 4) {
                    $('.chat-samples-create-button').removeClass('active');
                }
            }
        }
    })

    $('.chat-samples-input.text').on('input', (e) => {
        let result = [...e.target.value.matchAll(/\[TEXT[23]?]/g)];
        let variables = result.map((v) => {
            return v[0];
        })
        if(variables.length != 0) {
            $('.chat-samples-variables-block').css('display', 'grid');
            $('.chat-samples-variables-note').css('display', 'none');
            for(let i of ['', '2', '3']) {
                if(variables.includes(`[TEXT${i}]`) && validatedInputs[`var-text${i}`] == true && !$(`#var-text${i} > input`).val()) {
                    validatedInputsCount -= 1;
                    validatedInputs[`var-text${i}`] = false;
                    $(`#var-text${i} > span`).css('display', 'none');
                    $(`#var-text${i} > input`).css('display', 'block');
                    $(`#warning-var-text${i}`).css('display', '');
                    if(validatedInputsCount == 4) {
                        $('.chat-samples-create-button').removeClass('active');
                    }
                } else if (!variables.includes(`[TEXT${i}]`) && validatedInputs[`var-text${i}`] == false) {
                    validatedInputsCount += 1;
                    validatedInputs[`var-text${i}`] = true;
                    $(`#var-text${i} > span`).css('display', '');
                    $(`#var-text${i} > input`).css('display', '');
                    $(`#var-text${i} > input`).val('');
                    $(`#warning-var-text${i}`).css('display', 'none');
                    if(validatedInputsCount == 5) {
                        $('.chat-samples-create-button').addClass('active');
                    }
                }
            }
            if(variables.includes('[TEXT]') || variables.length == 0) {
                $('#warning-text2-not-text').css('display', 'none');
                $('#warning-text3-not-text').css('display', 'none');
            } else if(variables.includes('[TEXT2]') || variables.includes('[TEXT3]')) {
                validatedInputsCount -= 1;
                validatedInputs['text'] = false;
                if(validatedInputsCount == 4) {
                    $('.chat-samples-create-button').removeClass('active');
                }
                if(variables.includes('[TEXT2]')) {
                    $('#warning-text2-not-text').css('display', '');
                }
                if(variables.includes('[TEXT3]')) {
                    $('#warning-text3-not-text').css('display', '');
                }
            }
        } else {
            $('.chat-samples-variables-block').css('display', '');
            $('.chat-samples-variables-block input').val('');
        }
    })

    $('.chat-samples-checkbox-block').on('click', (e) => {
        let checkbox = e.target.querySelector('.chat-samples-checkbox');
        checkbox.checked = !checkbox.checked;
    })

    $('.chat-samples-create-button').on('click', (e) => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let name = $('.chat-samples-input.name').val();
        let description = $('.chat-samples-input.description').val();
        let text = $('.chat-samples-input.text').val();

        let variableText = $('#var-text input').val();
        let variableText2 = $('#var-text2 input').val();
        let variableText3 = $('#var-text3 input').val();
        let variables = {};
        if(variableText) {
            variables['[TEXT]'] = variableText;
        }
        if(variableText2) {
            variables['[TEXT2]'] = variableText2;
        }
        if(variableText3) {
            variables['[TEXT3]'] = variableText3;
        }

        let categories = [];
        $('.chat-samples-checkbox:checked').each((i, checkbox) => {
            categories.push(checkbox.id.replace('checkbox-', ''));
        })

        $.ajax({
            method: "post",
            url: "/chat/create_sample/",
            data: {csrfmiddlewaretoken: token, name:name, description: description, text: text, variables: JSON.stringify(variables), categories: JSON.stringify(categories)},
            success: (data) => {
                if(data['result'] == 'ok') {
                    $('.chat-samples-private .chat-samples-block').append(getSampleHTML(data['sample'], 'private'));
                    if(samplesData['private'].length == 0) {
                        $('.chat-samples-private .chat-samples-empty').css('display', 'none');
                        $('.chat-samples-private .chat-samples-button').css('display', 'none');
                    }
                    samplesData['private'].push(data['sample']);
                    $('.chat-samples-input').val('');
                    $('.chat-samples-checkbox').prop('checked', false);

                    $('#warning-name').css('display', '');
                    $('#warning-text').css('display', '');
                    $('#warning-var-text').css('display', 'none');
                    $('#warning-var-text2').css('display', 'none');
                    $('#warning-var-text3').css('display', 'none');
                    $('#warning-text2-not-text').css('display', 'none');
                    $('#warning-text3-not-text').css('display', 'none');

                    $('.chat-samples-variables-block').css('display', '');
                    $('.chat-samples-variables-block > span').css('display', '');
                    $('.chat-samples-variables-block > input').css('display', '');
                    $('.chat-samples-variables-note').css('display', '');

                    e.target.classList.remove('active');
                    $('#chat-samples-private').click();
                }
            },
            error: (data) => {
            }
        });
    })

    $('.chat-chat-textarea').on('input', (e) => {
        if(e.target.value.length == 1) {
            $('#open-samples').css('display', 'none');
            $('#send-message').css('display', 'flex');
        } else if(e.target.value.length == 0){
            $('#open-samples').css('display', '');
            $('#send-message').css('display', '');
        }
    })

    $('.chat-chat-textarea').on('paste', (e) => {
        $('#open-samples').css('display', 'none');
        $('#send-message').css('display', 'flex');
    })

    $(document).on('click', '.chat-menu-chat-block:not(.selected):not(.new)', (e) => {
        let pk = e.target.id.replace('menu-chat-', '');
        $.ajax({
            method: "get",
            url: "/chat/get_messages/",
            data: {pk: pk},
            success: (data) => {
                let htmlString = '';
                for(let message of data['messages']) {
                    let text = message['text'].length > 0 ? `<p id="text-${message['pk']}">${message['text']}</p>` : '';
                    let avatar = message['is_sender'] ? `<div class="chat-chat-message-avatar">${data['avatar']}</div>` : `<div class="chat-chat-message-logo"><img src="/${staticURL}img/logo.svg"></div>`;
                    let file = '';
                    if(message['file'] != null) {
                        file = message['is_sender'] ? `<a href="${message['file'][0]}" target="_blank" class="chat-chat-message-attachment">.${message['file'][1]}</a>` : `<div class="chat-chat-message-img-block"><img src="${message['file'][0]}" class="chat-chat-message-img"></div>`
                    }
                    let sample = message['sample'] != null ? `<span class="chat-chat-message-label">Шаблон:</span><p>${message['sample']}</p><span class="chat-chat-message-label">Запрос:</span>` : '';
                    htmlString += `<div class="chat-chat-message-block${message['is_sender'] ? '' : ' received'}" id="message-${message['pk']}">
                                    ${avatar}
                                    <div class="chat-chat-message">
                                        ${sample}
                                        ${text}
                                        ${file}
                                    </div>
                                    <div class="chat-chat-message-options">
                                        <div class="chat-chat-message-copy${!text ? ' only-image' : ''}" id="copy-message-${message['pk']}">
                                            <img src="/${staticURL}img/chat-copy.svg" alt="copy">
                                        </div>
                                        <div class="chat-chat-message-delete" id="delete-message-${message['pk']}">
                                            <img src="/${staticURL}img/chat-close.svg" alt="X">
                                        </div>
                                    </div>
                                </div>`;
                }

                $('.chat-new-chat-block').css('display', '');
                $('.chat-chat-field-content').html(htmlString);
                $('.chat-menu-chat-block.selected').removeClass('selected');
                e.target.classList.add('selected');
                if(window.innerWidth < 768) {
                    $('.m-header-menu-background').click();
                }
                isNew = false;
            },
            error: (data) => {
            }
        });
    })

    $('.chat-menu-chat-block.new').on('click', (e) => {
        $('.chat-chat-field-content').html('');
        $('.chat-new-chat-block').css('display', 'flex');
        $('.chat-menu-chat-block.selected').removeClass('selected');
        e.target.classList.add('selected');
        if(window.innerWidth < 768) {
            $('.m-header-menu-background').click();
        }
        isNew = true;
    })

    $('.m-chat-menu-new').on('click', (e) => {
        $('.chat-chat-field-content').html('');
        $('.chat-new-chat-block').css('display', 'flex');
        isNew = true;
    })

    function sendMessage() {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let text = $('.chat-chat-textarea').val();
        let validated = true;
        let formData = new FormData();
        formData.append('csrfmiddlewaretoken', token);
        formData.append('is_new', isNew);
        formData.append('text', text);
        let files = $('.chat-chat-textarea-file').prop('files');
        if(files.length > 0) {
            formData.append('file', files[0])
        }

        if(sampleOn) {
            formData.append('sample', $('.chat-chat-sample-block').attr('id').replace('chat-sample-block-', ''));
            for(let key of Object.keys(sampleVars)) {
                let value = $(`#chat-var-input-${key.slice(1, key.length - 1)}`).val();
                if(value.length > 0) {
                    sampleVars[key] = value;
                } else {
                    validated = false;
                    break;
                }
            }
            formData.append('variables', JSON.stringify(sampleVars));
        }
        if(validated) {
            if(sampleOn) {
                $('.chat-chat-sample-remove').click();
            }
            $('.chat-loader').css('visibility', 'visible');
            $('.chat-chat-textarea').val('');
            $('.chat-chat-textarea').attr('rows', 1);
            $('#open-samples').css('display', '');
            $('#send-message').css('display', '');
            $('#send-message').addClass('inactive');
            $('#remove-file').click();
            $.ajax({
                method: "post",
                url: "/chat/handle_request/",
                contentType: false,
                processData: false,
                data: formData,
                success: (data) => {
                    if(data['result'] == 'ok') {
                        let responseText = Object.keys(data['response']).includes('text') ? `<p id="text-${data['response']['message_pk']}">${data['response']['text']}</p>` : '';
                        let responseFile = Object.keys(data['response']).includes('file') ? `<div class="chat-chat-message-img-block"><img src="${data['response']['file']}" class="chat-chat-message-img"></div>` : '';
                        let requestFile = files.length > 0 ? `<a href="${data['attachment'][0]}" target="_blank" class="chat-chat-message-attachment">.${data['attachment'][1]}</a>` : '';
                        let requestSample = Object.keys(data).includes('sample') ? `<span class="chat-chat-message-label">Шаблон:</span><p>${data['sample']}</p><span class="chat-chat-message-label">Запрос:</span>` : '';
                        htmlString = `<div class="chat-chat-message-block received" id="message-${data['response']['message_pk']}">
                                        <div class="chat-chat-message-logo">
                                            <img src="/${staticURL}img/logo.svg">
                                        </div>
                                        <div class="chat-chat-message">
                                            ${responseText}
                                            ${responseFile}
                                        </div>
                                        <div class="chat-chat-message-options">
                                            <div class="chat-chat-message-copy${!responseText ? ' only-image' : ''}" id="copy-message-${data['response']['message_pk']}">
                                                <img src="/${staticURL}img/chat-copy.svg" alt="copy">
                                            </div>
                                            <div class="chat-chat-message-delete" id="delete-message-${data['response']['message_pk']}">
                                                <img src="/${staticURL}img/chat-close.svg" alt="X">
                                            </div>
                                        </div>
                                    </div>
                                    <div class="chat-chat-message-block" id="message-${data['message_pk']}">
                                        <div class="chat-chat-message-avatar">${data['avatar']}</div>
                                        <div class="chat-chat-message">
                                            ${requestSample}
                                            <p id="text-${data['message_pk']}">${data['text']}</p>
                                            ${requestFile}
                                        </div>
                                        <div class="chat-chat-message-options">
                                            <div class="chat-chat-message-copy" id="copy-message-${data['message_pk']}">
                                                <img src="/${staticURL}img/chat-copy.svg" alt="copy">
                                            </div>
                                            <div class="chat-chat-message-delete" id="delete-message-${data['message_pk']}">
                                                <img src="/${staticURL}img/chat-close.svg" alt="X">
                                            </div>
                                        </div>
                                    </div>`;
                        
                        $(`#${data['rest_requests']['key']}`).html(data['rest_requests']['value'])
                        $('.chat-chat-field-content').prepend(htmlString);
                        $('.chat-loader').css('visibility', '');
                        $('.chat-chat-field-area').scrollTop($('.chat-chat-field-area')[0].scrollHeight);
                        if(isNew) {
                            $('.chat-menu-chat-block.new').css('display', '');
                            $('.chat-menu-chat-block.selected').removeClass('selected');
                            $('.chat-menu-top').append(`<div class="chat-menu-chat-block selected" id="menu-chat-${data['chat_pk']}">
                                                            <img src="/${staticURL}img/chat-chat-icon.svg" alt="chat" class="chat-menu-img">
                                                            <span>${data['chat_name']}</span>
                                                            <div class="chat-menu-chat-delete" id="delete-chat-${data['chat_pk']}">
                                                                <img src="/${staticURL}img/chat-close.svg" alt="X">
                                                            </div>
                                                        </div>`);
                            isNew = false;
                        }
                    } else if(data['result'] == 'day limit') {
                        $('#notification-title').html('Максимум запросов');
                        $('#notification-text').html('Достигнут максимум суточных запросов по тарифу "Пробный". Чтобы увеличить количество запросов и разблокировать другие функции, выберите тариф. Также вы можете просто докупить запросы.');
                        $('#bg-notification > .chat-bg-buttons').css('display', '');
                        $('.chat-background').css('display', 'flex');
                        $('.chat-background-loader').css('visibility', '');
                        $('#bg-notification').css('display', 'flex');
                    } else if(data['result'] == 'month limit') {
                        $('#notification-title').html('Максимум запросов');
                        $('#notification-text').html(`Достигнут максимум запросов к нейросети "${data['ai']}" в этом месяце, либо ваш тариф не предполагает использование этой нейросети. Чтобы увеличить количество запросов, Вы можете выбрать другой тариф или докупить запросы.`);
                        $('#bg-notification > .chat-bg-buttons').css('display', '');
                        $('.chat-background').css('display', 'flex');
                        $('.chat-background-loader').css('visibility', '');
                        $('#bg-notification').css('display', 'flex');
                    } else if(data['result'] == 'failed') {
                        $('#notification-title').html('Упс. Что-то пошло не так');
                        $('#notification-text').html('Что-то пошло не так. Перезагрузите страницу и попробуйте заново.');
                        $('#bg-notification > .chat-bg-buttons').css('display', 'none');
                        $('.chat-background').css('display', 'flex');
                        $('.chat-background-loader').css('visibility', '');
                        $('#bg-notification').css('display', 'flex');
                    }
                    $('#send-message').removeClass('inactive');
                },
                error: (data) => {
                }
            });
        }
    }

    $('.chat-chat-textarea-send').on('click', () => {
        sendMessage();
    })

    // $('.chat-chat-textarea').on('keydown', (e) => {
    //     if(e.keyCode == '13' && !e.shiftKey) {
    //         sendMessage();
    //     }
    // })

    $('.chat-chat-textarea').on('input', (e) => {
        $('.chat-chat-textarea-ghost').val(e.target.value);
        let scrollHeight = $('.chat-chat-textarea-ghost').prop('scrollHeight');
        $('.chat-chat-textarea').attr('rows', scrollHeight / 28);
    })

    $(document).on('click', '.chat-menu-chat-delete', (e) => {
        e.stopPropagation();
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let id = e.target.id.replace('delete-chat-', '');
        $.ajax({
            method: "post",
            url: "/chat/delete_chat/",
            data: {csrfmiddlewaretoken: token, pk: id},
            success: (data) => {
                if(e.target.parentNode.classList.contains('selected')) {
                    $('.chat-menu-chat-block.new').click();
                }
                e.target.parentNode.remove();
                $('body').append(`<div class="chat-return-chat-block">
                                    <span>Чат успешно удалён</span>
                                    <span class="chat-return-chat-return" id="return-chat-${id}">Вернуть</span>
                                </div>`);

                window.setTimeout(() => {
                    $('.chat-return-chat-block').remove();
                }, 10000);
            },
            error: (data) => {
            }
        });
    })

    $(document).on('click', '.chat-return-chat-return', (e) => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let id = e.target.id.replace('return-chat-', '');
        $.ajax({
            method: "post",
            url: "/chat/return_chat/",
            data: {csrfmiddlewaretoken: token, pk: id},
            success: (data) => {
                $('.chat-return-chat-block').remove();
                $('.chat-menu-top').append(`<div class="chat-menu-chat-block" id="menu-chat-${id}">
                                                    <img src="/${staticURL}img/chat-chat-icon.svg" alt="chat" class="chat-menu-img">
                                                    <span>${data['chat_name']}</span>
                                                    <div class="chat-menu-chat-delete" id="delete-chat-${id}">
                                                        <img src="/${staticURL}img/chat-close.svg" alt="X">
                                                    </div>
                                                </div>`);
            },
            error: (data) => {
            }
        });
    })

    $(document).on('click', '.chat-chat-message-copy', (e) => {
        let id = e.target.id.replace('copy-message-', 'text-');
        var copyText = document.getElementById(id);
        navigator.clipboard.writeText(copyText.innerHTML.replace('<br>', '\n'));
    })

    $(document).on('click', '.chat-chat-message-delete', (e) => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let id = e.target.id.replace('delete-message-', '');
        $.ajax({
            method: "post",
            url: "/chat/delete_message/",
            data: {csrfmiddlewaretoken: token, pk: id},
            success: (data) => {
                $(`#message-${id}`).css('display', 'none');
                $(`#message-${id}`).after(`<div class="chat-chat-message-block chat-return-message-block${data['is_sender'] ? '' : ' received'}">
                                                <span>Сообщение успешно удалено</span>
                                                <span class="chat-return-message-return" id="return-message-${id}">Вернуть</span>
                                            </div>`);
            },
            error: (data) => {
            }
        });
    })

    $(document).on('click', '.chat-return-message-return', (e) => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let id = e.target.id.replace('return-message-', '');
        $.ajax({
            method: "post",
            url: "/chat/return_message/",
            data: {csrfmiddlewaretoken: token, pk: id},
            success: (data) => {
                e.target.parentNode.remove();
                $(`#message-${id}`).css('display', '');
            },
            error: (data) => {
            }
        });
    })

    $('.chat-chat-settings-block').on('click', () => {
        $('.chat-chat-settings').css('display', 'flex');
        $('.chat-chat-settings-bg').css('display', 'block');
    })

    $('.chat-chat-settings-bg').on('click', () => {
        $('.chat-chat-settings').css('display', '');
        $('.chat-chat-settings-bg').css('display', '');
    })

    $('.chat-chat-settings-selected-block:not(.blocked)').on('click', (e) => {
        if(e.target.classList.contains('chat-chat-settings-selected-block')) {
            e.target.classList.add('selected');
            $(`#${e.target.id.replace('ed', '')}`).css('display', 'flex');
            $('.chat-chat-select-bg').css('display', 'block');
        }
    })

    $('.chat-chat-select-bg').on('click', () => {
        $('.chat-chat-settings-selected-block.selected').removeClass('selected');
        $('.chat-chat-settings-select-block').css('display', '');
        $('.chat-chat-select-bg').css('display', '');
    })

    $('#attach-file').on('click', () => {
        if($('.chat-chat-textarea-file').prop('files').length == 0) {
            $('.chat-chat-textarea-file').click();
        } else {
            $('#bg-file').css('display', 'flex');
            $('.chat-background').css('display', 'flex');
        }
    })

    $('.chat-chat-textarea-file').on('click', (e) => {
        e.stopPropagation();
    })

    $('.chat-chat-textarea-file').on('change', (e) => {
        $('#bg-file').css('display', 'flex');
        $('.chat-background').css('display', 'flex');
        $('.chat-bg-file-block > span').html(e.target.files[0].name);
        $('.chat-chat-textarea-subblock svg').addClass('attached');
    })

    $('#remove-file').on('click', () => {
        $('.chat-chat-textarea-file').val('');
        $('#bg-file').css('display', '');
        $('.chat-background').css('display', '');
        $('.chat-bg-file-block > span').html('');
        $('.chat-chat-textarea-subblock svg').removeClass('attached');
    })

    $('#change-file').on('click', () => {
        $('.chat-chat-textarea-file').click();
    })

    $('.chat-chat-settings-select-option:not(.blocked)').on('click', (e) => {
        if(!e.target.classList.contains('selected')) {
            const token = $('input[name=csrfmiddlewaretoken]').val();
            let parentId = e.target.parentNode.id;
            let isImg = parentId == 'settings-select-img-ai';
            $.ajax({
                method: "post",
                url: "/chat/select_ai/",
                data: {csrfmiddlewaretoken: token, ai: e.target.innerHTML, is_img: isImg},
                success: (data) => {
                    $(`#${parentId} > .chat-chat-settings-select-option.selected`).removeClass('selected');
                    e.target.classList.add('selected');
                    $(`#${parentId.replace('select', 'selected')} > span`).html(e.target.innerHTML);
                    $('.chat-chat-select-bg').click();
                },
                error: (data) => {
                }
            });
        }
    })

    $('.chat-bg-request-input').on('keydown', (e) => {
        let symbol = String.fromCharCode(e.keyCode);
        let regEx = /[0-9]/
        if (!regEx.test(symbol) && ![8, 9, 13, 27].includes(e.keyCode)) {
            e.preventDefault();
        }
    })

    $('.chat-bg-request-input').on('change', (e) => {
        if(!requestLock) {
            requestLock = true;
            let ai = e.target.id.replace('request-', '');
            let oldQuantity = requestQuantity[ai];
            let newQuantity = e.target.value;
            let diff = newQuantity - oldQuantity;
            requestTotal += diff * requestPrice[ai];
            requestTotal = parseFloat(requestTotal.toFixed(2));
            requestQuantity[ai] += diff;
            $('.chat-bg-request-total').html(requestTotal + '&#8381;');
            requestLock = false;
        } else {
            e.preventDefault();
        }
    })

    $(document).on('click', '.chat-sample-block', (e) => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let id = e.target.id.replace('sample-', '');
        $.ajax({
            method: "get",
            url: "/chat/get_sample/",
            data: {csrfmiddlewaretoken: token, pk: id},
            success: (data) => {
                if(data['result'] == 'ok') {
                    $('.chat-chat-sample-block').remove();
                    $('.chat-chat-variable-block').remove();
                    sampleVars = {};
                    let htmlString = `<div class="chat-chat-sample-block" id="chat-sample-block-${id}">
                                        <span>${data['name']}</span>
                                        <div class="chat-chat-sample-remove">
                                            <img src="/${staticURL}img/chat-close.svg" alt="X">
                                        </div>
                                    </div>`;
                    let variables = data['variables'];
                    if(Object.keys(variables).includes('[TEXT]')) {
                        $('.chat-chat-textarea').prop('placeholder', variables['[TEXT]']);
                        $('.chat-chat-textarea').attr('id', 'chat-var-input-TEXT');
                        sampleVars['[TEXT]'] = '';
                        delete variables['[TEXT]'];
                        for(let [key, value] of Object.entries(variables)) {
                            sampleVars[key] = '';
                            htmlString += `<div class="chat-chat-variable-block" id="chat-var-block-${key.slice(1, key.length - 1)}">
                                            <span class="chat-auth-placeholder">${value}</span>
                                            <input type="text" class="chat-chat-variable-input" id="chat-var-input-${key.slice(1, key.length - 1)}">
                                        </div>`;
                        }
                    } else {
                        $('.chat-chat-textarea').prop('placeholder', 'Ввод не требуется');
                        $('.chat-chat-textarea').removeAttr('id');
                    }
                    $('.chat-chat-input-area').prepend(htmlString);
                    $('#chat-samples-close').click();
                    sampleOn = true;
                }
            },
            error: (data) => {
            }
        });
    })

    $(document).on('click', '.chat-chat-sample-remove', () => {
        $('.chat-chat-sample-block').remove();
        $('.chat-chat-variable-block').remove();
        $('.chat-chat-textarea').prop('placeholder', 'Сообщение');
        $('.chat-chat-textarea').removeAttr('id');
        sampleOn = false;
        sampleVars = {};
    })

    $(document).on('click', '.chat-chat-settings-context-block > div:not(.active)', (e) => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let value = e.target.classList[0].replace('chat-chat-settings-context-', '');
        $.ajax({
            method: "post",
            url: "/chat/set_context/",
            data: {csrfmiddlewaretoken: token, value: value},
            success: (data) => {
                if(data['result'] == 'ok') {
                    e.target.classList.add('active');
                    $(`.chat-chat-settings-context-${value == 'yes' ? 'no' : 'yes'}`).removeClass('active');
                }
            },
            error: (data) => {
            }
        });
    })

    $('.chat-new-sample-click').on('click', (e) => {
        $('.chat-chat-sample-remove').click();
        $('#remove-file').click();
        $('.chat-chat-textarea').val(e.target.querySelector('span').innerHTML);
        $('.chat-new-chat-block').css('display', '');
        $('.chat-background-content').css('display', '');
        $('#send-message').click();
    })

    $('.chat-new-top-open-samples').on('click', () => {
        $('#open-samples').click();
    })

    $('.chat-new-top-icon-block:not(.selected)').on('click', (e) => {
        if(window.innerWidth <= 1300) {
            let order = e.target.id.replace('new-icon-', '');
            $('.chat-new-top-icon-block').removeClass('selected');
            e.target.classList.add('selected');
            $('.chat-new-top-samples-block').css('display', 'none');
            $(`.chat-new-top-samples-block:nth-child(${order})`).css('display', 'flex');
            $('.chat-new-top-link').css('display', 'none');
            $(`.chat-new-top-link:nth-child(${order})`).css('display', 'flex');
        }
    })

    $('.m-chat-menu-open').on('click', () => {
        let menu = $('.chat-menu-block');

        $('.m-header-menu-background').css('display', 'block');
        menu.css('display', 'flex');
        menu.animate({
            'left': 0
        }, 500);
    })

    $('.m-header-menu-background').on('click', (e) => {
        let menu = $('.chat-menu-block');

        $('.m-header-menu-background').css('display', '');
        menu.animate({
            'left': `-${menu.outerWidth()}`
        }, 500, () => {
            menu.css('display', '');
        });
    })

    $('.m-chat-chat-options').on('click', (e) => {
        $('.chat-chat-textarea-options').css('display', 'flex');
        $('.m-chat-chat-options-background').css('display', 'flex');
    })

    $('.m-chat-chat-options-background').on('click', (e) => {
        $('.chat-chat-textarea-options').css('display', '');
        e.target.style.display = '';
    })

    $('.chat-payment-tariffs-submit').on('click', (e) => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let tariffPk = e.target.id.replace('payment-tariff-', '');
        $.ajax({
            method: "post",
            url: "/chat/get_payment_link/",
            data: {csrfmiddlewaretoken: token, subject: 'tariff', tariff_pk: tariffPk, count: $('.chat-payment-tariffs-months').val()},
            success: (data) => {
                if(data['result'] == 'ok') {
                    window.location.replace(data['link']);
                } else {
                    $('.chat-payment-bg').click();
                    $('#notification-title').html('Упс. Что-то пошло не так');
                    $('#notification-text').html('Что-то пошло не так. Перезагрузите страницу и попробуйте заново.');
                    $('#bg-notification > .chat-bg-buttons').css('display', 'none');
                    $('.chat-background').css('display', 'flex');
                    $('.chat-background-content').css('display', '');
                    $('#bg-notification').css('display', 'flex');
                }
            },
            error: (data) => {
            }
        });
    })

    $('.chat-payment-requests-submit').on('click', (e) => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let requests = [];
        $('.chat-bg-request-input').each((i, block) => {
            if(block.value > 0) {
                requests.push({'ai': block.id.replace('request-', ''), 'quantity': parseInt(block.value)})
            }
        })
        $.ajax({
            method: "post",
            url: "/chat/get_payment_link/",
            data: {csrfmiddlewaretoken: token, subject: 'requests', requests: JSON.stringify(requests)},
            success: (data) => {
                if(data['result'] == 'ok') {
                    window.location.replace(data['link']);
                } else {
                    $('.chat-payment-bg').click();
                    $('#notification-title').html('Упс. Что-то пошло не так');
                    $('#notification-text').html('Что-то пошло не так. Перезагрузите страницу и попробуйте заново.');
                    $('#bg-notification > .chat-bg-buttons').css('display', 'none');
                    $('.chat-background').css('display', 'flex');
                    $('.chat-background-content').css('display', '');
                    $('#bg-notification').css('display', 'flex');
                }
            },
            error: (data) => {
            }
        });
    })

    $('.chat-payment-business-submit').on('click', (e) => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            method: "post",
            url: "/chat/get_payment_link/",
            data: {csrfmiddlewaretoken: token, subject: 'business', cost: $('.chat-payment-business-balance').val()},
            success: (data) => {
                if(data['result'] == 'ok') {
                    window.location.replace(data['link']);
                } else {
                    $('.chat-payment-bg').click();
                    $('#notification-title').html('Упс. Что-то пошло не так');
                    $('#notification-text').html('Что-то пошло не так. Перезагрузите страницу и попробуйте заново.');
                    $('#bg-notification > .chat-bg-buttons').css('display', 'none');
                    $('.chat-background').css('display', 'flex');
                    $('.chat-background-content').css('display', '');
                    $('#bg-notification').css('display', 'flex');
                }
            },
            error: (data) => {
            }
        });
    })

    $('.chat-payment-promocode-submit').on('click', (e) => {
        const token = $('input[name=csrfmiddlewaretoken]').val();
        let promocode = $('.chat-payment-promocode').val();
        $.ajax({
            method: "post",
            url: "/chat/enter_promo_code/",
            data: {csrfmiddlewaretoken: token, promo_code: promocode},
            success: (data) => {
                if(data['result'] == 'ok') {
                    window.location.reload();
                } else {
                    $('.chat-payment-wrong-promocode').css('display', 'inline');
                }
            },
            error: (data) => {
            }
        });
    })

    window.addEventListener('resize', () => {
        if($('.chat-samples-container').css('display') == 'flex' && !$('#chat-samples-create').hasClass('selected')) {
            hideTags();
        }
    })
})