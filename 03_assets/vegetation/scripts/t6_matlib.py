"""material set per species (bark + leaf + extra slot) — shared by the library builder and the tests."""
import t6kit as K


def species_mats(S):
    B = S['bark']; nm = S['name']
    if B['tex'] == 'culm':          # bamboo culm: procedural (no bark scan fits) — waxy green with yellow streaks + node bands
        bark = K.mat_simple(f'MAT_T6_{nm}_CULM', '#6E8C3A', rough=.35, var_col='#A8A050', var_scale=3.0, coat=.3)
    else:
        bark = K.mat_bark(f'MAT_T6_{nm}_BARK', B['tex'], B.get('tint', '#FFFFFF'), B.get('moss', 0), B.get('moss_col', '#4E6B2C'),
                          B.get('lichen', 0), B.get('rough_add', 0), bleach=B.get('bleach', 0))
    mats = [bark]
    if S.get('leaves'):
        L = S.get('leaf', {})
        mats.append(K.mat_leaf(f'MAT_T6_{nm}_LEAF', S['leaves']['atlas'], transl=L.get('transl', .3), tint=L.get('tint', '#FFFFFF')))
    else:
        mats.append(K.mat_simple(f'MAT_T6_{nm}_NOLEAF', '#556B2F'))
    if S.get('pods'):
        mats.append(K.mat_simple(f'MAT_T6_{nm}_POD', '#DDF2D0', rough=.35, sss=.4, emission='#BFF5DA', em_strength=.6, transl=.3))   # subtle glow (Decision 01 §3)
    elif S.get('fungi'):
        mats.append(K.mat_simple(f'MAT_T6_{nm}_FUNGUS', '#B8925A', rough=.8, var_col='#6E4A2A', var_scale=30))
    elif S.get('beards'):
        mats.append(K.mat_leaf(f'MAT_T6_{nm}_BEARD', S['beards']['atlas'], transl=.3))
    else:
        mats.append(bark)
    if S.get('beards'):
        # beards use slot 1 (leaf) material in the generator → give them their own slot: remap in the builder
        pass
    return mats
