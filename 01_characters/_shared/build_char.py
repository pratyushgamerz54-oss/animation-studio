"""Build any character from its config.
Run:  python3 01_characters/_shared/build_char.py <folder> [version]
e.g.  python3 01_characters/_shared/build_char.py pratyush 002
Out:  01_characters/<folder>/blend/<folder>_v<version>.blend
"""
import sys, os, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def load_cfg(folder):
    d = os.path.join(HERE, '..', folder)
    sys.path.insert(0, d)
    return importlib.import_module(f'{folder}_config').CFG, d


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('-')]
    folder, ver = args[0], (args[1] if len(args) > 1 else '002')
    import charbuild as cb
    cfg, d = load_cfg(folder)
    out = os.path.join(d, 'blend', f'{folder}_v{ver}.blend')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cb.Char(cfg).build(out)
    print('SAVED', out)
