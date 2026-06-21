import re
from typing import List
from src.token import Token, TokenType

# Himpunan keyword dan fungsi bawaan yang dipetakan dari project_setup.md
KEYWORDS = {
    'Bener', 'Kaga', 'Kosong', # Boolean / Nilai Khusus yang masuk ke keyword
    'ama', 'atawa', 'bukan', 'kalo', 'kalo_kaga', 'laennya', 'buat', 'selagi', 
    'di', 'berenti', 'terusin', 'lewat', 'bikin', 'balikin', 'hasilin', 
    'fungsi_kecil', 'kelas', 'gue', 'emak', 'cobain', 'kecuali', 'akhirnya', 
    'angkat', 'pastiin', 'ambil', 'dari', 'sebagai', 'seluruhnya', 'bukan_lokal', 
    'pake', 'barengan', 'tungguin', 'cocok', 'kasus', 'apus', 'ialah'
}

BUILTINS = {
    'cetak', 'nanya', 'angka', 'desimal', 'teks', 'logika', 'komplek',
    'daftar', 'kumpulan', 'himpunan', 'kamus', 'himpunan_baku', 'mutlak',
    'buletin', 'pangkat', 'bagisisa', 'jumlah', 'paling_gede', 'paling_kecil',
    'panjang', 'jarak', 'daftarin', 'gabung', 'ulang', 'lanjut',
    'ulang_barengan', 'lanjut_barengan', 'balikin', 'urutin', 'semuanya',
    'salah_satu', 'jenis', 'ujikata', 'ujisub', 'tanda', 'bisa_dipanggil',
    'huruf', 'urutan', 'aski', 'biner', 'oktal', 'heksa', 'ambil_sifat',
    'atur_sifat', 'ada_sifat', 'apus_sifat', 'globalnya', 'lokalnya',
    'variabelnya', 'arah', 'bait', 'susunan_bait', 'liat_memori', 'evaluasi',
    'jalanin', 'kompilasi', 'buka', 'petain', 'saring', 'properti',
    'metode_statis', 'metode_kelas', '__ambil__', 'titik_renti', 'bentuk',
    'wakil', 'acak', 'tolong', 'potong', 'objek'
}

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"LexerError at line {line}, col {column}: {message}")

class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.pos = 0
        self.line = 1
        self.column = 1
        
        # Spesifikasi Regex (berurutan, rule terpanjang didahulukan)
        self.rules = [
            ('SKIP', r'[ \t]+'),
            ('COMMENT', r'#.*'),
            ('NEWLINE', r'\n'),
            ('STRING', r'"[^"]*"|\'[^\']*\''),
            ('NUMBER', r'\d+\.\d+|\d+'),
            ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),
            ('OPERATOR', r'==|!=|<=|>=|<|>|\+|-|\*|/|='),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('COMMA', r','),
            ('MISMATCH', r'.')
        ]
        
        self.regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.rules)
        self.scanner = re.compile(self.regex)

    def tokenize(self) -> List[Token]:
        tokens = []
        for match in self.scanner.finditer(self.source_code):
            kind = match.lastgroup
            value = match.group()
            
            if kind == 'SKIP' or kind == 'COMMENT':
                self.column += len(value)
                continue
            elif kind == 'NEWLINE':
                self.line += 1
                self.column = 1
                continue
            elif kind == 'MISMATCH':
                raise LexerError(f"Karakter Ilegal '{value}'", self.line, self.column)
            
            token_type = self._determine_token_type(kind, value)
            tokens.append(Token(token_type, value, self.line, self.column))
            self.column += len(value)
            
        tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return tokens
        
    def _determine_token_type(self, kind: str, value: str) -> TokenType:
        if kind == 'ID':
            if value in KEYWORDS:
                return TokenType.KEYWORD
            elif value in BUILTINS:
                return TokenType.BUILTIN
            else:
                return TokenType.IDENTIFIER
                
        mapping = {
            'STRING': TokenType.STRING,
            'NUMBER': TokenType.NUMBER,
            'OPERATOR': TokenType.OPERATOR,
            'LBRACE': TokenType.LBRACE,
            'RBRACE': TokenType.RBRACE,
            'LPAREN': TokenType.LPAREN,
            'RPAREN': TokenType.RPAREN,
            'COMMA': TokenType.COMMA
        }
        return mapping[kind]
