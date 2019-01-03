def rn(rows, column, room, bot):
    room[rows][column] = '>'
    column += 1
    room[rows][column] = bot
    return column


def dn(rows, column, room, bot):
    room[rows][column] = 'v'
    rows += 1
    room[rows][column] = bot
    return rows


def ln(rows, column, room, bot):
    room[rows][column] = '<'
    column -= 1
    room[rows][column] = bot
    return column


def un(rows, column, room, bot):
    room[rows][column] = '^'
    rows -= 1
    room[rows][column] = bot
    return rows
