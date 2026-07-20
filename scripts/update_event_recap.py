# -*- coding: utf-8 -*-
"""Add recap section, agenda highlights, and hero video to executive-exchange.html."""

from __future__ import annotations

import html as html_lib
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "executive-exchange.html"

AGENDA_IMAGES = {
    "CONNECT": ("https://media.gulfconnect.org/img/%E4%BC%9A%E5%9C%BA%E7%9B%9B%E5%86%B51.JPG", "Registration and networking"),
    "OPENING KEYNOTE": ("https://media.gulfconnect.org/img/%E6%9D%8E%E6%B5%B7%E5%B2%9A.JPG", "Opening keynote"),
    "OPENING REMARKS & PLATFORM LAUNCH": ("https://media.gulfconnect.org/img/Offical%20Launch%20of%20Gulf%20Connect.jpg", "Gulf Connect platform launch"),
    "LEAP EAST": ("https://media.gulfconnect.org/img/%E5%B7%B4%E6%96%AF%E7%8E%9B.JPG", "LEAP East remarks"),
    "BUILDING THE BACKBONE": ("https://media.gulfconnect.org/img/session1.jpg", "Session I: Building the Backbone"),
    "ROBOTICS: THE NEXT WORKFORCE": ("https://media.gulfconnect.org/img/session2.jpg", "Session II: Robotics"),
    "BUILDING AT SCALE": ("https://media.gulfconnect.org/img/session3.jpg", "Session III: Building at Scale"),
    "CAPITAL–ASSET SYSTEM REWIRING": ("https://media.gulfconnect.org/img/session4.jpg", "Session IV: Capital-Asset System Rewiring"),
    "THE NEW STARS": ("https://media.gulfconnect.org/img/%E4%B8%AD%E5%9B%BD%E4%B8%AD%E4%B8%9C%E6%96%B0%E5%85%B4%E4%BA%A7%E4%B8%9A%E6%A6%9C%E5%8D%95CEO1.JPG", "New Star Enterprises List launch"),
    "LIGHTER. STRONGER. CHEAPER.": ("https://media.gulfconnect.org/img/%E6%99%8F%E5%9F%B9%E6%9D%B0.JPG", "Advanced manufacturing"),
    "THE FUTURE IS BUILT": ("https://media.gulfconnect.org/img/session5.jpg", "Session V: Innovation in Action"),
    "STRATEGIC CONNECTIONS": ("https://media.gulfconnect.org/img/%E5%91%98%E5%B7%A5%E5%90%88%E7%85%A71.JPG", "Closed-door networking"),
}

HERO_BLOCK = """  <section class="event-hero event-hero-video-wrap">
    <video class="event-hero-video" autoplay muted loop playsinline webkit-playsinline preload="auto" poster="img/Our Mission_3.png">
      <source src="https://media.gulfconnect.org/video/Home_Earth.mp4" type="video/mp4">
    </video>
    <div class="event-hero-overlay"></div>
    <div class="event-hero-info event-hero-info-overlay">
      <div class="container">
        <p class="hero-eyebrow" style="text-align:center;margin-bottom:12px;">Gulf Connect x LEAP East</p>
        <h1 style="color:#fff;text-align:center;font-size:clamp(1.6rem,4vw,2.4rem);margin-bottom:12px;">Gulf Connect | Executive Exchange<br>中東通高層會客廳</h1>
        <p style="text-align:center;color:var(--gold-light);margin-bottom:8px;letter-spacing:0.05em;">Reshape Mindset / Activate Ecosystem / Achieve Milestone / Reach Destination</p>
        <p style="text-align:center;color:rgba(255,255,255,0.65);margin-bottom:32px;font-size:0.95rem;letter-spacing:0.04em;">思維重構 / 生態蓄勢 / 節點突破 / 行者致遠</p>
        <div class="event-meta">
          <div class="event-meta-item">
            <div class="label">Date</div>
            <div class="value">Wednesday, 8 July 2026<br>13:00 - 18:00</div>
          </div>
          <div class="event-meta-item">
            <div class="label">Venue</div>
            <div class="value">S421, Hong Kong Convention and Exhibition Centre (HKCEC)<br>1 Expo Drive, Wan Chai, Hong Kong</div>
          </div>
          <div class="event-meta-item">
            <div class="label">Format</div>
            <div class="value">Invitation-only Executive Exchange<br>约 100 位精选参与者</div>
          </div>
          <div class="event-meta-item">
            <div class="label">Language</div>
            <div class="value">Chinese &amp; English<br>中英双语</div>
          </div>
        </div>
        <div class="cta-group" style="justify-content:center;margin-top:32px;">
          <a href="#recap" class="btn btn-primary">Watch Event Recap</a>
          <a href="https://cxsurvey.ipsos.cn/survey2c/#/answer?id=SMDwBaKz4kbZML0HAI" class="btn btn-outline" target="_blank" rel="noopener">New Star Enterprises List</a>
        </div>
      </div>
    </div>
  </section>"""

RECAP_SECTION = """
  <section class="section section-cream" id="recap">
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
      <div class="recap-videos">
        <article class="recap-video-card">
          <h3>Event Recap</h3>
          <p class="recap-video-desc">Relive the key moments from Gulf Connect | Executive Exchange.</p>
          <video class="recap-video" controls playsinline preload="metadata" poster="https://media.gulfconnect.org/img/%E4%BC%9A%E5%9C%BA%E7%9B%9B%E5%86%B55.JPG">
            <source src="https://media.gulfconnect.org/video/recap.mp4" type="video/mp4">
          </video>
        </article>
        <article class="recap-video-card">
          <h3>Behind the Scenes</h3>
          <p class="recap-video-desc">A lighter look at the people and energy behind the event.</p>
          <video class="recap-video" controls playsinline preload="metadata" poster="https://media.gulfconnect.org/img/%E5%91%98%E5%B7%A5%E5%90%88%E7%85%A72.JPG">
            <source src="https://media.gulfconnect.org/video/blooper.mp4" type="video/mp4">
          </video>
        </article>
      </div>
      <div class="recap-gallery">
        <img src="https://media.gulfconnect.org/img/%E4%BC%9A%E5%9C%BA%E7%9B%9B%E5%86%B52.JPG" alt="Executive Exchange venue">
        <img src="https://media.gulfconnect.org/img/%E4%BC%9A%E5%9C%BA%E7%9B%9B%E5%86%B54.JPG" alt="Executive Exchange audience">
        <img src="https://media.gulfconnect.org/img/%E4%B8%AD%E5%9B%BD%E4%B8%AD%E4%B8%9C%E6%96%B0%E5%85%B4%E4%BA%A7%E4%B8%9A%E6%A6%9C%E5%8D%95CEO2.JPG" alt="New Star Enterprises List">
        <img src="https://media.gulfconnect.org/img/%E9%82%93%E5%BA%86%E6%97%AD.jpg" alt="Deng Qingxu, Sina Finance">
      </div>
    </div>
  </section>"""


def _extract_div_block(text: str, start: int) -> tuple[str, int]:
    depth = 0
    i = start
    while i < len(text):
        if text.startswith("<div", i):
            depth += 1
        elif text.startswith("</div>", i):
            depth -= 1
            if depth == 0:
                end = i + len("</div>")
                return text[start:end], end
        i += 1
    raise ValueError("Unclosed div block")


def _title_from_item(item_html: str) -> str:
    match = re.search(r'<div class="agenda-title">(.*?)</div>', item_html, re.DOTALL)
    if not match:
        return ""
    raw = re.sub(r"<[^>]+>", "", match.group(1))
    return html_lib.unescape(raw).strip()


def _wrap_agenda_item(item_html: str) -> str:
    title = _title_from_item(item_html)
    image = AGENDA_IMAGES.get(title)
    inner = item_html[len('<div class="agenda-item">'): -len("</div>")]
    if not image:
        return item_html
    src, alt = image
    return (
        '<div class="agenda-item has-media">\n'
        "          <div class=\"agenda-item-body\">"
        + inner
        + "</div>\n"
        f'          <div class="agenda-item-media"><img src="{escape(src)}" alt="{escape(alt)}"></div>\n'
        "        </div>"
    )


def _transform_agenda_timeline(timeline_html: str) -> str:
    marker = '<div class="agenda-item">'
    pos = 0
    parts: list[str] = []
    while True:
        start = timeline_html.find(marker, pos)
        if start == -1:
            parts.append(timeline_html[pos:])
            break
        parts.append(timeline_html[pos:start])
        block, end = _extract_div_block(timeline_html, start)
        parts.append(_wrap_agenda_item(block))
        pos = end
    return "".join(parts)


def main() -> None:
    html = HTML.read_text(encoding="utf-8")

    if 'class="executive-page"' not in html:
        html = html.replace("<body>", '<body class="executive-page">', 1)

    html = re.sub(
        r'  <section class="event-hero">.*?</section>\s*<section class="event-hero-info">.*?</section>',
        HERO_BLOCK,
        html,
        count=1,
        flags=re.DOTALL,
    )

    html = html.replace(
        '    <a href="#introduction" class="active">Intro 介绍</a>\n'
        '    <a href="#speakers">Speakers 嘉宾</a>\n'
        '    <a href="#agenda">Agenda 议程</a>',
        '    <a href="#recap" class="active">Recap 回顾</a>\n'
        '    <a href="#introduction">Intro 介绍</a>\n'
        '    <a href="#speakers">Speakers 嘉宾</a>\n'
        '    <a href="#agenda">Agenda 议程</a>',
    )

    if 'id="recap"' not in html:
        html = html.replace(
            '  <section class="section" id="introduction">',
            RECAP_SECTION + '\n\n  <section class="section" id="introduction">',
            1,
        )

    timeline_match = re.search(
        r'(<div class="agenda-timeline">)(.*?)(</div>\s*</div>\s*</section>\s*<section class="section section-navy")',
        html,
        flags=re.DOTALL,
    )
    if timeline_match:
        prefix, body, suffix = timeline_match.groups()
        new_body = _transform_agenda_timeline(body)
        html = html[: timeline_match.start()] + prefix + new_body + suffix + html[timeline_match.end() :]

    html = html.replace(
        '<h2 style="margin-bottom:16px;">Join Us at LEAP East 2026</h2>',
        '<h2 style="margin-bottom:16px;">Gulf Connect | Executive Exchange 2026</h2>',
    )
    html = html.replace(
        '<p style="max-width:600px;margin:0 auto 32px;color:rgba(255,255,255,0.75);">Invitation-only Executive Exchange. Register your interest today.</p>',
        '<p style="max-width:600px;margin:0 auto 32px;color:rgba(255,255,255,0.75);">Thank you to everyone who joined us at LEAP East Hong Kong. Explore the recap and agenda highlights below.</p>',
    )
    html = html.replace(
        '<a href="https://meeting.hyterp.cn/website/10024/register.html" class="btn btn-primary" target="_blank" rel="noopener">Event Registration</a>',
        '<a href="#recap" class="btn btn-primary">Watch Recap</a>',
        1,
    )

    HTML.write_text(html, encoding="utf-8")
    print(f"Updated {HTML}")


if __name__ == "__main__":
    main()
