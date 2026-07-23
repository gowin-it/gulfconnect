# -*- coding: utf-8 -*-
"""Apply second-draft instructions to executive-exchange.html."""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "executive-exchange.html"

ENTERPRISES = [
    ("阿尔法梯", "Alpha Ladder Group Pte Ltd"),
    ("", "BlueNexus Technologies Pte. Ltd."),
    ("上海西井科技股份有限公司", "Shanghai Westwell Technology Co., Ltd. (Westwell)"),
    ("安东油田服务集团", "Anton Oilfield Services Group"),
    ("", "EDGENEXT LEGEND DYNASTY PTE. LTD."),
    ("深圳桢观德芯科技有限公司", "Xpectvision Technology Co., Ltd."),
    ("百富环球科技有限公司", "PAX Global Technology Limited"),
    ("上海礼升生物科技有限公司", "Shanghai Lisheng Biotechnology"),
    ("苏州亿创特智能制造有限公司", "Suzhou Efficient Profile Intelligent Manufacturing Co., Ltd."),
    ("北京镁伽机器人股份有限公司", "MegaRobo Technologies Co., Ltd."),
    ("上海瑞柯恩激光技术股份有限公司", "Shanghai Raykeen Laser Technology Co., Ltd."),
    ("伊莱森清洁技术公司", "Blessent Clean Technologies"),
    ("北京银河通用机器人股份有限公司", "Beijing Galbot AI Co., Ltd."),
    ("上海蔚建科技有限公司", "Shanghai WeiBuild Technology Co., Ltd."),
    ("英矽智能", "Insilico Medicine Cayman TopCo"),
    ("", "Yalla Group Limited"),
    ("智慧互通科技股份有限公司", "Artificial Intelligent Interconnection Technology Co., Ltd."),
]


def media_block(paths: list[tuple[str, str]]) -> str:
    """Build agenda media HTML; multiple images become a mini stack."""
    imgs = "\n".join(
        f'            <img src="{html.escape(src)}" alt="{html.escape(alt)}">'
        for src, alt in paths
    )
    multi = " agenda-item-media-multi" if len(paths) > 1 else ""
    return f'          <div class="agenda-item-media{multi}">\n{imgs}\n          </div>'


def replace_agenda_media(text: str, title: str, paths: list[tuple[str, str]]) -> str:
    """Replace the first agenda-item-media after a given agenda-title."""
    pattern = re.compile(
        rf'(<div class="agenda-title">{re.escape(title)}</div>.*?)'
        r'(<div class="agenda-item-media(?: agenda-item-media-multi)?">.*?</div>)',
        re.S,
    )
    new_media = media_block(paths)
    new_text, n = pattern.subn(rf"\1{new_media}", text, count=1)
    if n != 1:
        raise SystemExit(f"Failed to replace media for: {title}")
    return new_text


def build_enterprise_cards() -> str:
    cards = []
    for zh, en in ENTERPRISES:
        zh_html = f'<div class="enterprise-zh">{html.escape(zh)}</div>' if zh else ""
        cards.append(
            f"""        <article class="enterprise-card">
{zh_html}
          <div class="enterprise-en">{html.escape(en)}</div>
        </article>"""
        )
    return "\n".join(cards)


def build_gallery_items() -> str:
    gallery_dir = ROOT / "img3" / "gallery"
    # Prefer a curated order for the carousel
    preferred = [
        "会场盛况1.JPG",
        "OpeningKeynote.jpg",
        "OpeningRemark1.jpg",
        "OpeningRemark2.jpg",
        "OpeningRemark3.jpg",
        "Offical Launch of Gulf Connect.jpg",
        "会场盛况3.JPG",
        "刘智元.JPG",
        "邓庆旭.jpg",
        "徐莹.JPG",
        "巴斯玛.JPG",
        "李海岚.JPG",
        "session1.jpg",
        "Robotics.jpg",
        "session2.jpg",
        "session3.jpg",
        "session4.jpg",
        "NewStars1.jpg",
        "NewStars2.jpg",
        "中国中东新兴产业榜单CEO1.JPG",
        "中国中东新兴产业榜单CEO2.JPG",
        "LighterStrongerCheaper.jpg",
        "session5.jpg",
        "StrategicConnections.jpg",
        "会场盛况4.JPG",
        "会场盛况5.JPG",
        "员工合照1.JPG",
        "员工合照2.JPG",
    ]
    existing = {p.name: p for p in gallery_dir.iterdir() if p.is_file()}
    ordered = [existing[name] for name in preferred if name in existing]
    for name, path in sorted(existing.items()):
        if path not in ordered:
            ordered.append(path)

    items = []
    for i, path in enumerate(ordered):
        rel = f"img3/gallery/{path.name}"
        alt = path.stem
        items.append(
            f'          <button type="button" class="photo-carousel-item" data-index="{i}" aria-label="{html.escape(alt)}">'
            f'<img src="{html.escape(rel)}" alt="{html.escape(alt)}" loading="lazy"></button>'
        )
    return "\n".join(items), len(ordered)


def main() -> None:
    text = HTML_PATH.read_text(encoding="utf-8")

    # 1) Hero: remove meta + CTAs, add partner logos
    hero_old = re.search(
        r'(<p style="text-align:center;color:rgba\(255,255,255,0\.65\);margin-bottom:32px;font-size:0\.95rem;letter-spacing:0\.04em;">思維重構 / 生態蓄勢 / 節點突破 / 行者致遠</p>)\s*'
        r'<div class="event-meta">.*?</div>\s*'
        r'<div class="cta-group".*?</div>',
        text,
        re.S,
    )
    if not hero_old:
        raise SystemExit("Hero meta/cta block not found")

    hero_new = (
        hero_old.group(1)
        + """
        <div class="hero-partner-logos" aria-label="Partner logos">
          <img src="img3/1.GulfConnect.png" alt="Gulf Connect">
          <img src="img3/2.LEAPEast.png" alt="LEAP East">
          <img src="img3/3.SinaFinance.png" alt="Sina Finance">
        </div>"""
    )
    text = text[: hero_old.start()] + hero_new + text[hero_old.end() :]

    # 2) Event nav tabs
    nav_new = """  <nav class="event-nav">
    <a href="#introduction"><span class="event-nav-en">Intro</span><span class="event-nav-zh">介绍</span></a>
    <a href="#speakers"><span class="event-nav-en">Speakers</span><span class="event-nav-zh">嘉宾</span></a>
    <a href="#agenda"><span class="event-nav-en">Agenda</span><span class="event-nav-zh">议程</span></a>
    <a href="#recap"><span class="event-nav-en">Recap</span><span class="event-nav-zh">回顾</span></a>
    <a href="#media"><span class="event-nav-en">Media</span><span class="event-nav-zh">媒体</span></a>
    <a href="#new-stars"><span class="event-nav-en">New Star List</span><span class="event-nav-zh">新星榜单</span></a>
  </nav>"""
    text, n = re.subn(r"<nav class=\"event-nav\">.*?</nav>", nav_new, text, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("event-nav not replaced")

    # 3) Agenda subtitle
    text = text.replace(
        "<p>Updated on July 6, Subject to Change</p>",
        "<p>8 July 2026, Hong Kong Convention &amp; Exhibition Centre</p>",
    )

    # 4) Agenda photo replacements
    text = replace_agenda_media(
        text,
        "OPENING KEYNOTE",
        [("img3/OpeningKeynote.jpg", "Opening keynote")],
    )
    text = replace_agenda_media(
        text,
        "OPENING REMARKS &amp; PLATFORM LAUNCH",
        [
            ("img3/OpeningRemark1.jpg", "Opening remarks 1"),
            ("img3/OpeningRemark2.jpg", "Opening remarks 2"),
            ("img3/OpeningRemark3.jpg", "Opening remarks 3"),
        ],
    )
    text = replace_agenda_media(
        text,
        "ROBOTICS: THE NEXT WORKFORCE",
        [("img3/Robotics.jpg", "Robotics session")],
    )
    text = replace_agenda_media(
        text,
        "THE NEW STARS",
        [
            ("img3/NewStars1.jpg", "New Stars 1"),
            ("img3/NewStars2.jpg", "New Stars 2"),
        ],
    )
    text = replace_agenda_media(
        text,
        "LIGHTER. STRONGER. CHEAPER.",
        [("img3/LighterStrongerCheaper.jpg", "Lighter Stronger Cheaper")],
    )
    text = replace_agenda_media(
        text,
        "STRATEGIC CONNECTIONS",
        [("img3/StrategicConnections.jpg", "Strategic Connections")],
    )

    # 5) Recap: keep intro text only (move video/gallery to Media)
    recap_new = """  <section class="section section-cream" id="recap">
    <div class="container">
      <div class="section-header">
        <div class="gold-line"></div>
        <h2>Event Recap</h2>
        <p>Highlights from Gulf Connect | Executive Exchange at LEAP East Hong Kong, 8 July 2026</p>
      </div>
      <div class="recap-intro">
        <p>On 8 July 2026, Gulf Connect convened leaders from sovereign investment institutions, industrial groups, technology companies, policymakers and cross-border investment communities across Asia and the GCC for a full-day executive exchange during LEAP East Hong Kong.</p>
        <p>From the official launch of Gulf Connect to panel discussions on infrastructure, robotics, capital connectivity and innovation, the gathering brought together more than 100 selected participants for strategic dialogue, long-term collaboration and regional engagement.</p>
        <p>2026年7月8日，Gulf Connect 在香港 LEAP East 期间举办高层会客厅，汇聚来自亚洲与海湾地区的主权投资机构、产业集团、科技企业、政策制定者与跨境投资社群代表，围绕平台发布、产业协同、资本连接与创新生态展开全天深度交流。</p>
      </div>
    </div>
  </section>
"""
    gallery_html, gallery_count = build_gallery_items()
    media_section = f"""  <section class="section" id="media">
    <div class="container">
      <div class="section-header">
        <div class="gold-line"></div>
        <h2>Media</h2>
        <p>Event film and photo highlights | 活动影像与照片</p>
      </div>

      <div class="media-video-wrap">
        <video class="recap-video media-video" controls playsinline preload="metadata" controlsList="nodownload noplaybackrate" disablePictureInPicture poster="https://media.gulfconnect.org/img/poster.jpg">
          <source src="https://media.gulfconnect.org/video/recap.mp4" type="video/mp4">
        </video>
      </div>

      <div class="photo-carousel" data-count="{gallery_count}" aria-label="Event photo carousel">
        <button type="button" class="photo-carousel-nav prev" aria-label="Previous photo">&#10094;</button>
        <div class="photo-carousel-track">
{gallery_html}
        </div>
        <button type="button" class="photo-carousel-nav next" aria-label="Next photo">&#10095;</button>
      </div>
      <p class="photo-carousel-hint">Swipe or click a photo to enlarge · 左右滑动浏览，点击照片放大</p>
    </div>
  </section>

  <div class="lightbox" id="photo-lightbox" hidden>
    <button type="button" class="lightbox-close" aria-label="Close">&times;</button>
    <button type="button" class="lightbox-nav prev" aria-label="Previous">&#10094;</button>
    <img class="lightbox-image" alt="">
    <button type="button" class="lightbox-nav next" aria-label="Next">&#10095;</button>
  </div>
"""

    enterprise_section = f"""  <section class="section section-cream" id="new-stars">
    <div class="container">
      <div class="section-header">
        <div class="gold-line"></div>
        <h2>New Star Enterprise List</h2>
        <p>中国－中东产业新星企业榜单</p>
      </div>
      <div class="new-stars-intro">
        <p>During the event, Gulf Connect officially introduced the China–Middle East New Star Enterprises List — a long-term reference framework for Middle Eastern sovereign investors, government institutions and industrial stakeholders seeking globally competitive Chinese enterprises with strong regional growth potential.</p>
        <p>活动期间，Gulf Connect 正式发布「中国－中东产业新星企业榜单」，为中东主权投资机构、政府与产业方识别具备区域增长潜力的中国企业提供长期参考。</p>
      </div>
      <div class="enterprise-grid">
{build_enterprise_cards()}
      </div>
    </div>
  </section>
"""

    # Replace old recap section through bottom CTA section
    pattern = re.compile(
        r"  <section class=\"section section-cream\" id=\"recap\">.*?"
        r"  <section class=\"section section-navy\" style=\"text-align:center;\">.*?</section>\n",
        re.S,
    )
    bottom_cta = """  <section class="section section-navy" style="text-align:center;">
    <div class="container">
      <h2 style="margin-bottom:16px;">Gulf Connect | Executive Exchange 2026</h2>
      <p style="max-width:600px;margin:0 auto;color:rgba(255,255,255,0.75);">Thank you to everyone who joined us at LEAP East Hong Kong. Explore the recap, media and New Star Enterprises List above.</p>
    </div>
  </section>
"""
    replacement = recap_new + "\n" + media_section + "\n" + enterprise_section + "\n" + bottom_cta
    text, n = pattern.subn(replacement, text, count=1)
    if n != 1:
        raise SystemExit("recap/bottom block not replaced")

    # Intro section still has New Star blurb — keep it; link CTA in intro box optional
    HTML_PATH.write_text(text, encoding="utf-8")
    print(f"Updated {HTML_PATH}")
    print(f"Gallery items: {gallery_count}")


if __name__ == "__main__":
    main()
