from collections import namedtuple

STATIC_KIND = "static"
FIELD_KIND = "field"
ARG_KIND = "arg"
VAR_KIND = "var"
SymbolEntry = namedtuple('SymbolEntry', ['type', 'kind', 'index'])


class SymbolTable:
    def __init__(self):
        self.counters = {
            STATIC_KIND: 0,
            FIELD_KIND: 0,
            ARG_KIND: 0,
            VAR_KIND: 0
        }

        self.class_symbols = {}
        self.subroutine_symbols = None

    def start_subroutine(self):
        self.counters[ARG_KIND] = 0
        self.counters[VAR_KIND] = 0
        self.subroutine_symbols = {}

    def define(self, name, type, kind):
        index = self.counters[kind]
        self.counters[kind] += 1
        entry = SymbolEntry(type, kind, index)

        if kind in (STATIC_KIND, FIELD_KIND):
            self.class_symbols[name] = entry
        else:
            self.subroutine_symbols[name] = entry

    def varCount(self, kind):
        return self.counters[kind]

    def kindOf(self, name: str):
        entry = self.subroutine_symbols.get(name)
        if entry:
            return entry.kind
        entry = self.class_symbols.get(name)
        if entry:
            return entry.kind

        return None

    def typeOf(self, name: str):
        entry = self.subroutine_symbols.get(name)
        if entry:
            return entry.type
        entry = self.class_symbols.get(name)
        if entry:
            return entry.type

        return None

    def indexOf(self, name: str):
        entry = self.subroutine_symbols.get(name)
        if entry:
            return entry.index
        entry = self.class_symbols.get(name)
        if entry:
            return entry.index
        return None
