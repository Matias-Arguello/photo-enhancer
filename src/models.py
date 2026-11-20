from gfpgan import GFPGANer
from config import CONFIG, MODEL_BG
from zeroscratches import EraseScratches
from src.utils import bgr_to_pil, pil_to_bgr
import streamlit as st
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer


class ImageEnhancer:
    """Clase para manejar el modelo GFPGAN y el procesamiento de imágenes."""

    def __init__(self):
        self.model = None
        self.model_with_bg = None
        self._scratch_eraser = None

    @st.cache_resource
    def load_model_with_background(_self):
        """Carga GFPGAN con RealESRGAN (mejora caras + fondo)."""
        with st.spinner("Cargando GFPGAN + RealESRGAN..."):
            model_bg = RRDBNet(
                num_in_ch=MODEL_BG["num_in_ch"],      
                num_out_ch=MODEL_BG["num_out_ch"],    
                num_feat=MODEL_BG["num_feat"],        
                num_block=MODEL_BG["num_block"],       
                num_grow_ch=MODEL_BG["num_grow_ch"],     
                scale=MODEL_BG["scale"]
            )

            bg_upsampler = RealESRGANer(
                scale=2,
                model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth',
                model=model_bg,
                tile=400,
                tile_pad=10,
                pre_pad=0,
                half=False
            )

            model = GFPGANer(
                model_path=CONFIG['model_url'],
                upscale=CONFIG['upscale'],
                arch=CONFIG['arch'],
                channel_multiplier=CONFIG['channel_multiplier'],
                bg_upsampler=bg_upsampler
            )
        return model

    @property
    def scratch_eraser(self):
        if self._scratch_eraser is None:
            self._scratch_eraser = EraseScratches()
        return self._scratch_eraser
    
    def _remove_scratches(self, image_bgr):
        """Elimina rayas o grietas antes de pasar a GFPGAN."""
        pil_img = bgr_to_pil(image_bgr)
        restored_rgb = self.scratch_eraser.erase(pil_img)
        restores_bgr = pil_to_bgr(restored_rgb)
        return restores_bgr

    @st.cache_resource
    def load_model_simple(_self):
        """Carga GFPGAN para la mejora de caras + fondos."""
        model = GFPGANer(
            model_path=CONFIG["model_url"],
            upscale=CONFIG["upscale"],
            arch=CONFIG["arch"],
            channel_multiplier=CONFIG["channel_multiplier"],
            bg_upsampler=None
        )
        return model
    
    def enhance(self, image_bgr, repair_scratches=False, enhance_background=False):
        """
        Mejora una imagen con opciones configurables.
        
        Args:
            image_bgr: Imagen en formato BGR
            repair_scratches: Si True, repara grietas primero
            enhance_background: Si True, usa RealESRGAN para el fondo
        """
        if repair_scratches:
            st.info("🔧 Reparando grietas y arañazos...")
            image_bgr = self._remove_scratches(image_bgr)

        # Seleccionar modelo según opciones
        if enhance_background:
            st.info("✨ Mejorando caras y fondo...")
            if self.model_with_bg is None:
                self.model_with_bg = self.load_model_with_background()
            model = self.model_with_bg
        else:
            st.info("✨ Mejorando caras...")
            if self.model is None:
                self.model = self.load_model_simple()
            model = self.model

        _, _, restored_img = model.enhance(
            image_bgr,
            has_aligned=False,
            only_center_face=False,
            paste_back=True,
            weight=CONFIG["enhancement_weight"]
        )

        return restored_img