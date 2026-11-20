PAGE_CONFIG = {
    "page_title": "Mejorador de Fotos con IA",
    "page_icon": "✨",
    "layout": "centered"
}


CONFIG = {
    # Modelo GFPGAN
    "model_url": "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.3.pth",
    "upscale": 2,
    "arch": "clean",
    "channel_multiplier": 2,
    "enhancement_weight": 0.5,

    # Formatos permitidos
    "allowed_formats": ['jpg', 'jpeg', 'png']
}

MODEL_BG = {
    # Modelo ReakESRGAN
    "num_in_ch": 3,        # 3 canales de entrada (RGB)
    "num_out_ch": 3,       # 3 canales de salida (RGB)
    "num_feat":64,         # 64 características
    "num_block": 23,       # 23 bloques
    "num_grow_ch": 32,     # 32 canales de crecimiento
    "scale": 2             # Escala 2x
}