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
        'password_description': 'Returns a random sequence of {:d} characters.',
        'password_message': 'A generated password of {:d} characters is <b>{}</b>.',
        'password_length_invalid': 'A password cannot be shorter than {:d} characters or longer than {:d}!',

        'rand_num_title': 'Get a random number!',
        'rand_num_description': 'Returns a random number from {:d} to {:d}.',
        'rand_num_message': 'A random number between {:d} and {:d} is *{:d}*.',
        'rand_num_from_zero_description': 'Returns a random number up to {:d}.',
        'rand_num_from_zero_message': 'A random number up to {:d} is *{:d}*.',

        'yes_no_title': 'Yes or no?',
        'yes_no_description': 'Gives you the answer on your question.',
        'yes_no_message': 'You asked me: <i>{}</i>\nI think <b>{}</b>.',

        'rand_item_title': 'Get a random item!',
        'rand_item_description': 'Returns a random item from your list.',
        'rand_item_message': 'From: <i>{}</i>\nI choose: <b>{}</b>.',

        'help': """Hello, dear friend! Can I help you? Maybe, do you need to decide something? Or get a random number?

I'm able to respond to the following commands:
`/coin` (or `/flip_coin`) - returns either *heads* or *tails*.
`/yesno` (or `/yes_or_no`) - returns either *yes* or *no*.
`/number [from] <up to>` - returns a *random number* between _from_ (1 if omitted) and _up to_.
`/list item 1, item 2...` - returns a *random item* from your _list_ (a semicolon can be used as a separator too).
`/seq [length]` (aliases `/password` and `/sequence`)  - returns a password of _length_ ({:d} if omitted) characters.

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
        'password_description': 'Возвращает случайную последовательность из {:d} символов.',
        'password_message': 'Сгенерированный пароль из {:d} символов: <b>{}</b>.',
        'password_length_invalid': 'Пароль не может состоять меньше чем из {:d} символов или больше чем из {:d}!',

        'rand_num_title': 'Получить случайное число!',
        'rand_num_description': 'Возвращает случайное число от {:d} до {:d}.',
        'rand_num_message': 'Случайное число между {:d} и {:d}: *{:d}*.',
        'rand_num_from_zero_description': 'Возвращает случайное число до {:d}.',
        'rand_num_from_zero_message': 'Случайное число до {:d}: *{:d}*.',

        'yes_no_title': 'Да или нет?',
        'yes_no_description': 'Даёт ответ на вопрос.',
        'yes_no_message': 'Ты спросил меня: <i>{}</i>\nЯ думаю, что <b>{}</b>.',

        'rand_item_title': 'Получить случайный элемент списка!',
        'rand_item_description': 'Возвращает случайный элемент из указанного списка.',
        'rand_item_message': 'Из: <i>{}</i>\nЯ выбираю: <b>{}</b>.',

        'help': """Привет, друг! Помочь тебе с принятием решения? Или, может быть, хочешь получить случайное число? 

Я умею отвечать на следующие команды:
`/coin` (или `/flip_coin`) - возвращает *орла* или *решку*.
`/yesno` (или `/yes_or_no`) - возвращает *да* или *нет*.
`/number [от] <до>` - возвращает *случайное число* между _от_ (1, если опущено) и _до_.
`/list вариант 1, вариант 2...` - возвращает *случайный элемент* из _списка_ (в качестве разделителя может выступать и \
точка с запятой (*;*)).
`/seq [длина]` (псевдонимы: `/password` и `/sequence`)  - возвращает пароль из _длина_ ({:d}, если опущена) символов.

Обрати внимание, что ты можешь использовать меня в любом чате через inline-режим!
"""
    }

}
