L = {

    'en': {
        'heads': 'Heads',
        'tails': 'Tails',
        'yes': 'yes',
        'no': 'no',
        'usage': 'Usage',
        'from': 'from',
        'to': 'to',
        'item': 'item',

        'flip_coin_title': 'Flip a coin!',
        'flip_coin_description': 'Returns either heads or tails.',

        'password_title': 'Generate a password!',
        'password_description': 'Returns a random sequence of %i characters.',
        'password_message': 'A generated password of %i characters is <b>%s</b>.',
        'password_length_invalid': 'A password cannot be shorter than 6 characters or longer than 2048!',

        'rand_num_title': 'Get a random number!',
        'rand_num_description': 'Returns a random number from %i to %i.',
        'rand_num_message': 'A random number between %i and %i is *%i*.',
        'rand_num_from_zero_message': 'A random number up to %i is *%i*.',

        'yes_no_title': 'Yes or no?',
        'yes_no_description': 'Gives you the answer on your question.',
        'yes_no_message': 'You asked me: <i>%s</i>\nI think <b>%s</b>.',

        'rand_item_title': 'Get a random item!',
        'rand_item_description': 'Returns a random item from your list.',
        'rand_item_message': 'From: <i>%s</i>\nI choose: <b>%s</b>.',

        'help': """Hello, dear friend! Can I help you? Maybe, do you need to decide something? Or get a random number?

I'm able to respond to the following commands:
`/coin` (or `/flip_coin`) - returns either *heads* or *tails*.
`/yesno` (or `/yes_or_no`) - returns either *yes* or *no*.
`/number [from] <up to>` - returns a *random number* between _from_ (1 if omitted) and _up to_.
`/list item 1, item 2...` - returns a *random item* from your _list_ (a semicolon can be used as a separator too).
`/seq [length]` (aliases `/password` and `/sequence`)  - returns a password of _length_ (8 if omitted) characters.

Note that you may use me in any chat via the inline mode!
"""
    },

    'ru': {
        'heads': 'Орёл',
        'tails': 'Решка',
        'yes': 'да',
        'no': 'нет',
        'usage': 'Использование',
        'from': 'от',
        'to': 'до',
        'item': 'вариант',

        'flip_coin_title': 'Бросить монетку!',
        'flip_coin_description': 'Возвращает выпавшую сторону монеты.',

        'password_title': 'Сгенерировать пароль!',
        'password_description': 'Возвращает случайную последовательность из %i символов.',
        'password_message': 'Сгенерированный пароль из %i символов: <b>%s</b>.',
        'password_length_invalid': 'Пароль не может состоять меньше чем из 6 символов или больше чем из 2048!',

        'rand_num_title': 'Получить случайное число!',
        'rand_num_description': 'Возвращает случайное число от %i до %i.',
        'rand_num_message': 'Случайное число между %i и %i: *%i*.',
        'rand_num_from_zero_message': 'Случайное число до %i: *%i*.',

        'yes_no_title': 'Да или нет?',
        'yes_no_description': 'Даёт ответ на вопрос.',
        'yes_no_message': 'Ты спросил меня: <i>%s</i>\nЯ думаю, что <b>%s</b>.',

        'rand_item_title': 'Получить случайный элемент списка!',
        'rand_item_description': 'Возвращает случайный элемент из указанного списка.',
        'rand_item_message': 'Из: <i>%s</i>\nЯ выбираю: <b>%s</b>.',

        'help': """Привет, друг! Помочь тебе с принятием решения? Или, может быть, хочешь получить случайное число? 

Я умею отвечать на следующие команды:
`/coin` (или `/flip_coin`) - возвращает *орла* или *решку*.
`/yesno` (или `/yes_or_no`) - возвращает *да* или *нет*.
`/number [от] <до>` - возвращает *случайное число* между _от_ (1, если опущено) и _до_.
`/list вариант 1, вариант 2...` - возвращает *случайный элемент* из _списка_ (в качестве разделителя может выступать и \
точка с запятой (*;*)).
`/seq [длина]` (псевдонимы: `/password` и `/sequence`)  - возвращает пароль из _длина_ (8, если опущена) символов.

Обрати внимание, что ты можешь использовать меня в любом чате через inline-режим!
"""
    }

}
