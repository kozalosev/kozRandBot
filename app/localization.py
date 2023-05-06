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
        'rand_num_from_zero_to_one_message': 'A random number between 0 and 1 is *{:f}*.',

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
`/seq [length]` (aliases `/password` and `/sequence`) - returns a password of _length_ ({:d} if omitted) characters.
`/seqс [length]` (aliases `/cseq`  and `/passwd`) - returns a password of _length_ ({:d} if omitted) characters consisting of only digits and latins.

Note that you may use me in any chat via the inline mode!
""",

        'commands': {
            'coin': "returns either heads or tails",
            'yesno': "returns either yes or no",
            'number': "returns a random number between boundaries",
            'list': "returns a random item from a list",
            'seq': "returns a password of N characters",
            'seqc': "returns a password of N characters consisting of only digits and latins",
        }
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
        'rand_num_from_zero_to_one_message': 'Случайное число между 0 и 1: *{:f}*.',

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
`/seq [длина]` (псевдонимы: `/password` и `/sequence`) - возвращает пароль из _длина_ ({:d}, если опущена) символов.
`/seqс [длина]` (псевдонимы `/cseq` и `/passwd`) - возвращает пароль из _длина_ ({:d}, если опущена) символов, причём исключительно из латиницы и цифр.

Обрати внимание, что ты можешь использовать меня в любом чате через inline-режим!
""",

        'commands': {
            'coin': "возвращает орла или решку",
            'yesno': "возвращает да или нет",
            'number': "возвращает случайное число в указанном диапазоне",
            'list': "возвращает случайный элемент из списка",
            'seq': "возвращает пароль из N символов",
            'seqc': "возвращает пароль из N символов латиницы и цифр",
        }
    },
    
    'pt': {
        'heads': 'Cara',
        'tails': 'Coroa',
        'yes': 'sim',
        'no': 'não',
        'usage': 'Uso',
        'from': 'de',
        'to': 'a',
        'item': 'item',

        'flip_coin_title': 'Jogue uma moeda!',
        'flip_coin_description': 'Retorna cara ou coroa.',

        'password_title': 'Gerar uma senha!',
        'password_description': 'Retorna uma sequência aleatória de caracteres {:d}.',
        'password_message': 'Uma senha gerada com {:d} caracteres é <b>{}</b>.',
        'password_length_invalid': 'Uma senha não pode ter menos de {:d} caracteres ou mais de {:d}!',

        'rand_num_title': 'Obter um número aleatório!',
        'rand_num_description': 'Retorna um número aleatório entre {:d} e {:d}.',
        'rand_num_message': 'Um número aleatório entre {:d} e {:d} é *{:d}*.',
        'rand_num_from_zero_description': 'Retorna um número aleatório até {:d}.',
        'rand_num_from_zero_message': 'Um número aleatório até {:d} é *{:d}*.',
        'rand_num_from_zero_to_one_message': 'Um número aleatório entre 0 and 1 e *{:f}*.',

        'yes_no_title': 'Sim ou não?',
        'yes_no_description': 'Envia uma resposta para sua pergunta.',
        'yes_no_message': 'Você me perguntou: <i>{}</i>\nEu acho que <b>{}</b>.',

        'rand_item_title': 'Obter um item aleatório!',
        'rand_item_description': 'Retorna um item aleatório da sua lista.',
        'rand_item_message': 'De: <i>{}</i>\nEu escolho: <b>{}</b>.',

        'help': """Olá, meu amigo, posso ajudar? Talvez você precise decidir alguma coisa? Ou obter um número aleatório?

Sou capaz de responder aos seguintes comandos:
`/coin` (ou `/flip_coin`) - retorna *cara* ou *coroa*.
`/yesno` (ou `/yes_or_no`) - retorna *sim* ou *não*.
`/number [de] <até>` - retorna um *número aleatório* entre o valor em _de_ (1, se não tiver sido definido) e o valor em _até_.
`/list item 1, item 2...` - retorna um *item aleatório* da sua _lista_ (é possível usar ponto-e-vírgula para separar itens).
`/seq [comprimento]` (alternativas `/password` ou `/sequence`) - retorna uma senha com o número de caracteres definido em _comprimento_ ({:d}, se não tiver sido definido).
`/seqс [comprimento]` (alternativas `/cseq` ou `/passwd`) - retorna uma senha com o número de caracteres definido em _comprimento_ ({:d}, se não tiver sido definido), consistindo apenas de números e letras latinas.

Lembre-se que pode usar estes comandos em qualquer conversa através do modo inline!
""",

        'commands': {
            'coin': "retorna cara ou coroa",
            'yesno': "retorna sim ou não",
            'number': "retorna um número aleatório no intervalo especificado",
            'list': "retorna um item aleatório da sua lista",
            'seq': "retorna uma senha de N caracteres",
            'seqc': "retorna uma senha de N caracteres latinos e dígitos",
        }
    },

}
