from typing import List, Dict, Any
from src.schemas.llm_outputs import SlideGenerationOutput, SlideItem

class SlideTemplate:
    """
    Render cấu trúc Slide sang định dạng hiển thị (HTML/SVG).
    Thiết kế theo phong cách Premium, hiện đại cho GD.
    """
    
    @staticmethod
    def render_to_html(slide_output: SlideGenerationOutput) -> str:
        """Render toàn bộ bài giảng thành 1 trang HTML trình chiếu (Carousel-like)."""
        html = [
            "<div class='presentation-container'>",
            f"<style>{SlideTemplate._get_css()}</style>"
        ]
        
        for i, slide in enumerate(slide_output.slides):
            html.append(SlideTemplate._render_slide_item(slide, i + 1))
            
        html.append("</div>")
        return "\n".join(html)

    @staticmethod
    def _render_slide_item(slide: SlideItem, index: int) -> str:
        icon = {"title": "🎯", "content": "📖", "exercise": "✏️",
                "image": "🖼️", "summary": "📋"}.get(slide.slide_type, "📄")
        
        html = [
            f"<div class='slide slide-{slide.slide_type}' id='slide-{index}'>",
            f"  <div class='slide-header'>",
            f"    <span class='slide-icon'>{icon}</span>",
            f"    <h2>{slide.title}</h2>",
            f"  </div>",
            f"  <div class='slide-content'>",
            f"    <ul class='bullet-list'>"
        ]
        
        for bullet in slide.bullets:
            html.append(f"      <li>{bullet}</li>")
            
        html.append("    </ul>")
        
        # Nếu có bài tập
        if slide.questions:
            html.append("    <div class='exercise-box'>")
            html.append("      <p>📝 <b>Bài tập rèn luyện:</b></p>")
            for q in slide.questions[:1]: # Show 1st question as teaser
                html.append(f"      <div class='mini-question'>{q.get('question')}</div>")
            html.append("    </div>")
            
        html.append("  </div>")
        html.append(f"  <div class='slide-footer'>Slide {index}</div>")
        html.append("</div>")
        
        return "\n".join(html)

    @staticmethod
    def _get_css() -> str:
        return """
        .presentation-container {
            font-family: 'Outfit', 'Inter', sans-serif;
            color: #2D3436;
            max-width: 800px;
            margin: auto;
        }
        .slide {
            background: #FFFFFF;
            border-radius: 16px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
            border: 1px solid #F0F0F0;
            min-height: 400px;
            display: flex;
            flex-direction: column;
        }
        .slide-title { background: linear-gradient(135deg, #6C5CE7, #A29BFE); color: white; }
        .slide-title h2 { color: white; text-align: center; font-size: 2.5em; }
        .slide-header { display: flex; align-items: center; margin-bottom: 25px; border-bottom: 2px solid #F0F0F0; padding-bottom: 15px; }
        .slide-icon { font-size: 2em; margin-right: 15px; }
        .slide-content { flex: 1; }
        .bullet-list { list-style: none; padding: 0; }
        .bullet-list li { margin: 15px 0; font-size: 1.1em; position: relative; padding-left: 25px; }
        .bullet-list li::before { content: '•'; color: #6C5CE7; font-weight: bold; position: absolute; left: 0; font-size: 1.5em; top: -5px; }
        .exercise-box { background: #F9F9FF; border-left: 4px solid #00B894; padding: 15px; margin-top: 20px; border-radius: 8px; }
        .mini-question { font-style: italic; color: #636E72; font-size: 0.9em; margin-top: 5px; }
        .slide-footer { margin-top: auto; font-size: 0.8em; color: #B2BEC3; text-align: right; }
        """
