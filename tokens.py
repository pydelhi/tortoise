# For Lexical Analysis, we define Tokens for our language

TOKEN_HTML = 'html'
TOKEN_EOF = 'eof'
TOKEN_VAR = 'variable'
TOKEN_BLOCK = 'block'
TOKEN_COMMENT = 'comment'
TOKEN_BLOCK_END = 'block_end'

TOKEN_DICT = {
        '{{': TOKEN_VAR,
        '}}': TOKEN_VAR,
        '{%': TOKEN_BLOCK,
        '%}': TOKEN_BLOCK,
        '{#': TOKEN_COMMENT,
        '#}': TOKEN_COMMENT,
}

TOKEN_BEGIN_SCOPE = 'scope_begin'
TOKEN_END_SCOPE = 'scope_end'
TOKEN_INITIAL = 'initial'
