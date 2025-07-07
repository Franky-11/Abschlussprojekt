
from __future__ import annotations

import streamlit as st
from base64 import b64encode
from pathlib import Path
from typing import Union

# -----------------------------------------------------
# Hauptfunktion
# -----------------------------------------------------

def set_watermark(
    image: Union[str, Path] | None = None,
    *,
    light_opacity: float = 0.06,
    dark_opacity: float = 0.12,
    size: str = "cover",
    position: str = "center",
) -> None:
    """Legt das (grau skaliertes) Wasserzeichen hinter die komplette App.

    Parameters
    ----------
    image : str | Path | None
        Pfad zum Bild; *None* → verwendet JPEG neben dieser Datei.
    light_opacity : float
        Transparenz im Light-Mode (0–1).
    dark_opacity : float
        Transparenz im Dark-Mode (typisch höher für Kontrast).
    size : str
        CSS-`background-size` ("cover", "contain" oder Pixel-/Prozent-Wert).
    position : str
        CSS-`background-position` (z. B. "center", "top left", "50% 50%" …).
    """

    # ---------------------------------------------
    # Bildpfad auflösen
    # ---------------------------------------------
    if image is None:
        # Standard: die JPEG-Datei liegt im selben Ordner wie diese Python-Datei
        image = Path(__file__).with_name("uuid=1084AF7B-E86A-498C-A5CB-D28982234D6A&code=001&library=1&type=1&mode=2&loc=true&cap=true.jpeg")
    img_path = Path(image)

    if not img_path.exists():
        raise FileNotFoundError(
            f"Watermark image not found – expected at: {img_path.resolve()}"
        )

    # ---------------------------------------------
    # Bild in Base64 encodieren
    # ---------------------------------------------
    b64 = b64encode(img_path.read_bytes()).decode()

    # ---------------------------------------------
    # CSS-Block zusammenstellen & in die App injizieren
    # ---------------------------------------------
    css = f"""
    <style>
    /* ------------------------------------------------- */
    /*  Basis: .stApp als Stacking Context               */
    /* ------------------------------------------------- */
    .stApp {{ position: relative; }}

    /* ------------------------------------------------- */
    /*  Wasserzeichen – Light Theme                      */
    /* ------------------------------------------------- */
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;                         /* top/right/bottom/left:0 */
        pointer-events: none;             /* nicht klick-blockend    */
        background: url(data:image/jpeg;base64,{b64}) no-repeat {position};
        background-size: {size};
        filter: grayscale(100%);
        opacity: {light_opacity};
        mix-blend-mode: multiply;         /* sanft in hellen BGs     */
        z-index: 0;                       /* vor .stApp-BG, hinter UI*/
    }}

    /* ------------------------------------------------- */
    /*  Dark Theme                                       */
    /* ------------------------------------------------- */
    @media (prefers-color-scheme: dark) {{
        .stApp::before {{
            opacity: {dark_opacity};
            filter: grayscale(100%) brightness(180%) contrast(120%);
            mix-blend-mode: screen;       /* auf dunklen BGs sichtbar*/
        }}
    }}

    /* ------------------------------------------------- */
    /*  Widgets wieder nach vorn holen                   */
    /* ------------------------------------------------- */
    .stApp > * {{ position: relative; z-index: 1; }}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)


# -----------------------------------------------------
# Quickstart / Debug-Aufruf
# -----------------------------------------------------
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    set_watermark()
    st.markdown("## Demo: Wasserzeichen aktiv ✨")

