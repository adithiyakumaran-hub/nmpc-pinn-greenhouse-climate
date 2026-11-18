import os
import xml.etree.ElementTree as ET

def create_crop_disease_drawio():
    """Generates the exact draw.io XML matching the user's uploaded image."""
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-11-18T00:00:00.000Z" agent="Antigravity" version="24.0.0">
  <diagram id="crop_disease_flowchart" name="Overall Architecture">
    <mxGraphModel dx="1200" dy="1600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="900" pageHeight="1400" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- ================= START ================= -->
        <mxCell id="start" value="&lt;b&gt;Start&lt;/b&gt;" style="rounded=1;arcSize=50;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="375" y="30" width="150" height="36" as="geometry" />
        </mxCell>

        <!-- ================= CONTAINER 1: USER INTERFACE ================= -->
        <mxCell id="c_ui" value="&lt;b style=&quot;font-size:13px;&quot;&gt;User Interface (Mobile / Web)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=6 3;strokeColor=#000000;strokeWidth=1.5;fillColor=none;verticalAlign=top;spacingTop=8;fontFamily=Helvetica;" vertex="1" parent="1">
          <mxGeometry x="80" y="95" width="740" height="110" as="geometry" />
        </mxCell>

        <mxCell id="ui_open" value="Open Application" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="110" y="135" width="180" height="46" as="geometry" />
        </mxCell>

        <mxCell id="ui_lang" value="Select Language" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="360" y="135" width="180" height="46" as="geometry" />
        </mxCell>

        <mxCell id="ui_upload" value="Upload Leaf Image" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="610" y="135" width="180" height="46" as="geometry" />
        </mxCell>

        <!-- ================= CONNECTOR BOX: SEND IMAGE ================= -->
        <mxCell id="send_box" value="&lt;b&gt;Send Image + Request&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;HTTP POST (multipart/form-data)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="330" y="235" width="240" height="48" as="geometry" />
        </mxCell>

        <!-- ================= CONTAINER 2: BACKEND SERVER ================= -->
        <mxCell id="c_backend" value="&lt;b style=&quot;font-size:13px;&quot;&gt;Backend Server (FastAPI - Port 8000)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=6 3;strokeColor=#000000;strokeWidth=1.5;fillColor=none;verticalAlign=top;spacingTop=8;fontFamily=Helvetica;" vertex="1" parent="1">
          <mxGeometry x="45" y="310" width="810" height="570" as="geometry" />
        </mxCell>

        <mxCell id="be_handler" value="Request Handler" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;fontStyle=1;" vertex="1" parent="1">
          <mxGeometry x="350" y="345" width="200" height="38" as="geometry" />
        </mxCell>

        <mxCell id="be_prep" value="&lt;b&gt;Image Preprocessing&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;(Resize, Normalization)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="335" y="405" width="230" height="46" as="geometry" />
        </mxCell>

        <!-- SUB-CONTAINER: AI MODELS -->
        <mxCell id="c_models" value="&lt;b style=&quot;font-size:12px;&quot;&gt;Heterogeneous AI Models (Sequential Inference)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=5 3;strokeColor=#000000;strokeWidth=1.5;fillColor=none;verticalAlign=top;spacingTop=6;fontFamily=Helvetica;" vertex="1" parent="1">
          <mxGeometry x="60" y="475" width="780" height="115" as="geometry" />
        </mxCell>

        <mxCell id="m_yolo" value="&lt;b&gt;YOLOv8n&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;(Disease Detection)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="85" y="515" width="200" height="52" as="geometry" />
        </mxCell>

        <mxCell id="m_resnet" value="&lt;b&gt;ResNet-18&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;(Classification)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="350" y="515" width="200" height="52" as="geometry" />
        </mxCell>

        <mxCell id="m_vit" value="&lt;b&gt;Vision Transformer&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;(Classification)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="615" y="515" width="200" height="52" as="geometry" />
        </mxCell>

        <mxCell id="be_ensemble" value="&lt;b&gt;Ensemble Voting &amp;amp; Confidence Calibration&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;(Final Prediction: Disease Class + Confidence + Bounding Box)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="205" y="615" width="490" height="48" as="geometry" />
        </mxCell>

        <mxCell id="be_adv" value="&lt;b&gt;Multilingual Advisory Generation&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;(Explanation + Treatment &amp;amp; Prevention Advice)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="205" y="685" width="490" height="48" as="geometry" />
        </mxCell>

        <mxCell id="be_db" value="&lt;b&gt;Store Results in Database&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;(User uploads, Predictions, Bounding boxes, Chat history, Timestamps)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="205" y="755" width="490" height="48" as="geometry" />
        </mxCell>

        <mxCell id="be_json" value="&lt;b&gt;Generate JSON Response&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;(Results + Advice)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="205" y="825" width="490" height="42" as="geometry" />
        </mxCell>

        <!-- ================= CONTAINER 3: RESULTS DELIVERY ================= -->
        <mxCell id="c_delivery" value="&lt;b style=&quot;font-size:13px;&quot;&gt;Results Delivery (Web / Mobile)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=6 3;strokeColor=#000000;strokeWidth=1.5;fillColor=none;verticalAlign=top;spacingTop=8;fontFamily=Helvetica;" vertex="1" parent="1">
          <mxGeometry x="45" y="905" width="810" height="115" as="geometry" />
        </mxCell>

        <mxCell id="del_disp" value="&lt;b&gt;Display Detected Disease&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;(with Bounding Box)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="75" y="945" width="220" height="52" as="geometry" />
        </mxCell>

        <mxCell id="del_score" value="&lt;b&gt;Show Confidence Score&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;and Treatment Advice&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="340" y="945" width="220" height="52" as="geometry" />
        </mxCell>

        <mxCell id="del_chat" value="&lt;b&gt;Chatbot Interaction&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;(Multilingual)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="605" y="945" width="220" height="52" as="geometry" />
        </mxCell>

        <!-- ================= DECISION & END ================= -->
        <mxCell id="dec_another" value="&lt;b&gt;Upload Another Image?&lt;/b&gt;" style="rhombus;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="325" y="1045" width="250" height="55" as="geometry" />
        </mxCell>

        <mxCell id="end" value="&lt;b&gt;End&lt;/b&gt;" style="rounded=1;arcSize=50;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="375" y="1135" width="150" height="36" as="geometry" />
        </mxCell>

        <!-- ================= CAPTION ================= -->
        <mxCell id="caption" value="&lt;b style=&quot;font-size:13px;&quot;&gt;Figure 1.&lt;/b&gt; Overall architecture of the proposed framework." style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontFamily=Times New Roman;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="250" y="1200" width="400" height="30" as="geometry" />
        </mxCell>

        <!-- ================= EDGES / ARROWS ================= -->
        <!-- Start -> UI Open -->
        <mxCell id="e_start_ui" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="start" target="ui_lang" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- UI Open -> UI Lang -->
        <mxCell id="e_ui1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="ui_open" target="ui_lang" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- UI Lang -> UI Upload -->
        <mxCell id="e_ui2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="ui_lang" target="ui_upload" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- UI Upload -> Send Box -->
        <mxCell id="e_upload_send" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="ui_upload" target="send_box" parent="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="700" y="259" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- Send Box -> Request Handler -->
        <mxCell id="e_send_handler" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="send_box" target="be_handler" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Handler -> Preprocessing -->
        <mxCell id="e_h_p" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="be_handler" target="be_prep" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Preprocessing -> Models Container / YOLO -->
        <mxCell id="e_p_models" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="be_prep" target="m_resnet" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- YOLO -> ResNet -->
        <mxCell id="e_y_r" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="m_yolo" target="m_resnet" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- ResNet -> ViT -->
        <mxCell id="e_r_v" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="m_resnet" target="m_vit" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Models -> Ensemble -->
        <mxCell id="e_m_ens" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="m_resnet" target="be_ensemble" parent="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="450" y="600" />
              <mxPoint x="450" y="600" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- Ensemble -> Advisory -->
        <mxCell id="e_ens_adv" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="be_ensemble" target="be_adv" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Advisory -> Database -->
        <mxCell id="e_adv_db" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="be_adv" target="be_db" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Database -> JSON Response -->
        <mxCell id="e_db_json" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="be_db" target="be_json" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- JSON Response -> Results Delivery Container (Score) -->
        <mxCell id="e_json_del" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="be_json" target="del_score" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Results Delivery internal: Display -> Score -->
        <mxCell id="e_d1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="del_disp" target="del_score" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Results Delivery internal: Score -> Chatbot -->
        <mxCell id="e_d2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="del_score" target="del_chat" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Results Delivery -> Decision -->
        <mxCell id="e_del_dec" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="del_score" target="dec_another" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Decision -> End (No) -->
        <mxCell id="e_dec_no" value="No" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontFamily=Helvetica;fontSize=12;" edge="1" source="dec_another" target="end" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Decision -> Upload Leaf Image (Yes Loop) -->
        <mxCell id="e_dec_yes" value="Yes" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;fontFamily=Helvetica;fontSize=12;" edge="1" source="dec_another" target="ui_upload" parent="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="870" y="1073" />
              <mxPoint x="870" y="158" />
            </Array>
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''
    with open('fig1_crop_disease_architecture.drawio', 'w', encoding='utf-8') as f:
        f.write(xml_content.strip())
    print("Created fig1_crop_disease_architecture.drawio successfully!")

def create_greenhouse_nmpc_pinn_drawio():
    """Generates the Greenhouse Tomato NMPC+PINN Control Architecture in the EXACT same flowchart architecture."""
    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2026-11-18T00:00:00.000Z" agent="Antigravity" version="24.0.0">
  <diagram id="greenhouse_nmpc_pinn_flowchart" name="Greenhouse NMPC Architecture">
    <mxGraphModel dx="1200" dy="1600" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="900" pageHeight="1400" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- ================= START ================= -->
        <mxCell id="start" value="&lt;b&gt;Start (Control Step k)&lt;/b&gt;" style="rounded=1;arcSize=50;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="360" y="30" width="180" height="36" as="geometry" />
        </mxCell>

        <!-- ================= CONTAINER 1: SUPERVISORY & TELEMETRY ================= -->
        <mxCell id="c_sup" value="&lt;b style=&quot;font-size:13px;&quot;&gt;Supervisory &amp;amp; Sensor Acquisition Layer (Sampling Ts = 60 s)&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=6 3;strokeColor=#000000;strokeWidth=1.5;fillColor=none;verticalAlign=top;spacingTop=8;fontFamily=Helvetica;" vertex="1" parent="1">
          <mxGeometry x="80" y="95" width="740" height="110" as="geometry" />
        </mxCell>

        <mxCell id="s_targets" value="&lt;b&gt;Agronomic Setpoints&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;(Diurnal Temp, RH, CO₂, VPD)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="105" y="135" width="190" height="48" as="geometry" />
        </mxCell>

        <mxCell id="s_weather" value="&lt;b&gt;Weather Forecast d(k)&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;(Solar Radiation, Ambient Temp)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="355" y="135" width="190" height="48" as="geometry" />
        </mxCell>

        <mxCell id="s_sensors" value="&lt;b&gt;Atmospheric Sensors&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;(T_air, W_air, C_CO2 Telemetry)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="605" y="135" width="190" height="48" as="geometry" />
        </mxCell>

        <!-- ================= CONNECTOR BOX: DISPATCH ================= -->
        <mxCell id="dispatch_box" value="&lt;b&gt;Transmit State &amp;amp; Disturbance Vector&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;Synchronous Edge Bus (MQTT / Modbus-TCP)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="325" y="235" width="250" height="48" as="geometry" />
        </mxCell>

        <!-- ================= CONTAINER 2: EDGE OPTIMIZATION ENGINE ================= -->
        <mxCell id="c_edge" value="&lt;b style=&quot;font-size:13px;&quot;&gt;Edge Controller: Delay-Compensated NMPC &amp;amp; Observer Pipeline&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=6 3;strokeColor=#000000;strokeWidth=1.5;fillColor=none;verticalAlign=top;spacingTop=8;fontFamily=Helvetica;" vertex="1" parent="1">
          <mxGeometry x="45" y="310" width="810" height="570" as="geometry" />
        </mxCell>

        <mxCell id="be_delay" value="&lt;b&gt;Actuator Delay Augmentation&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;(1st-Order Padé Filters: Heating 60s, Vents 30s, Fog 10s, CO₂ 20s)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="215" y="345" width="470" height="44" as="geometry" />
        </mxCell>

        <mxCell id="be_state" value="&lt;b&gt;8-State Microclimate Reconstruction&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;x(k) = [T_air, W, C_CO2, T_leaf, x_d,heat, x_d,vent, x_d,fog, x_d,co2]^T&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="215" y="405" width="470" height="46" as="geometry" />
        </mxCell>

        <!-- SUB-CONTAINER: ESTIMATION & STABILITY -->
        <mxCell id="c_models" value="&lt;b style=&quot;font-size:12px;&quot;&gt;Heterogeneous Virtual Sensing &amp;amp; Stability Engines&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=5 3;strokeColor=#000000;strokeWidth=1.5;fillColor=none;verticalAlign=top;spacingTop=6;fontFamily=Helvetica;" vertex="1" parent="1">
          <mxGeometry x="60" y="475" width="780" height="115" as="geometry" />
        </mxCell>

        <mxCell id="m_pm" value="&lt;b&gt;Penman-Monteith&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;Thermodynamics Loss&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="85" y="515" width="200" height="52" as="geometry" />
        </mxCell>

        <mxCell id="m_pinn" value="&lt;b&gt;PINN Canopy Observer&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;Estimates T_leaf &amp;amp; Transpiration E_T&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="350" y="515" width="200" height="52" as="geometry" />
        </mxCell>

        <mxCell id="m_dare" value="&lt;b&gt;DARE Stability Engine&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;Terminal Penalty Matrix P (ρ&amp;lt;1.0)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="615" y="515" width="200" height="52" as="geometry" />
        </mxCell>

        <mxCell id="be_nmpc" value="&lt;b&gt;Constrained Nonlinear Model Predictive Control (NMPC OCP)&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;Interior-Point Solver: Min Tracking Error + Energy Cost s.t. Bounds &amp;amp; Rate Limits&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="195" y="615" width="510" height="48" as="geometry" />
        </mxCell>

        <mxCell id="be_opt" value="&lt;b&gt;Extract Optimal First Actuator Commands u*(k)&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;Heating Valve Q_heat, Natural Vents A_v, Fogging Rate q_fog, CO₂ Valve U_co2&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="195" y="685" width="510" height="48" as="geometry" />
        </mxCell>

        <mxCell id="be_chain" value="&lt;b&gt;Decentralized Resource Tokenisation&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;Log Energy &amp;amp; Water Savings to Ethereum Smart Contract Ledger (GHRC)&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="195" y="755" width="510" height="48" as="geometry" />
        </mxCell>

        <mxCell id="be_sig" value="&lt;b&gt;Actuator Signal Generation &amp;amp; Rate Clamping&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;PWM / 4–20 mA Industrial Control Signals&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="195" y="825" width="510" height="42" as="geometry" />
        </mxCell>

        <!-- ================= CONTAINER 3: PHYSICAL GLASSHOUSE ================= -->
        <mxCell id="c_glasshouse" value="&lt;b style=&quot;font-size:13px;&quot;&gt;Physical Glasshouse Environment &amp;amp; Plant Response&lt;/b&gt;" style="rounded=0;whiteSpace=wrap;html=1;dashed=1;dashPattern=6 3;strokeColor=#000000;strokeWidth=1.5;fillColor=none;verticalAlign=top;spacingTop=8;fontFamily=Helvetica;" vertex="1" parent="1">
          <mxGeometry x="45" y="905" width="810" height="115" as="geometry" />
        </mxCell>

        <mxCell id="gh_act" value="&lt;b&gt;Physical Actuators&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;Pipes, Motors, Fog, Injector&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="75" y="945" width="220" height="52" as="geometry" />
        </mxCell>

        <mxCell id="gh_plant" value="&lt;b&gt;Tomato Canopy &amp;amp; Microclimate&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;Coupled Thermal, Vapor, CO₂ Balance&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="340" y="945" width="220" height="52" as="geometry" />
        </mxCell>

        <mxCell id="gh_feedback" value="&lt;b&gt;State Evolution x(k+1)&lt;/b&gt;&lt;br/&gt;&lt;span style=&quot;font-size:11px;&quot;&gt;Measured Microclimate Feedback&lt;/span&gt;" style="rounded=0;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="605" y="945" width="220" height="52" as="geometry" />
        </mxCell>

        <!-- ================= DECISION & END ================= -->
        <mxCell id="dec_loop" value="&lt;b&gt;Control Horizon Step k &amp;lt; K_sim?&lt;/b&gt;" style="rhombus;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="315" y="1045" width="270" height="55" as="geometry" />
        </mxCell>

        <mxCell id="end" value="&lt;b&gt;End (Simulation Complete)&lt;/b&gt;" style="rounded=1;arcSize=50;whiteSpace=wrap;html=1;strokeColor=#000000;strokeWidth=1.5;fillColor=#ffffff;fontFamily=Helvetica;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="360" y="1135" width="180" height="36" as="geometry" />
        </mxCell>

        <!-- ================= CAPTION ================= -->
        <mxCell id="caption" value="&lt;b style=&quot;font-size:13px;&quot;&gt;Figure 1.&lt;/b&gt; Proposed delay-compensated NMPC and PINN observer control architecture for tomato greenhouse microclimate regulation." style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontFamily=Times New Roman;fontSize=13;" vertex="1" parent="1">
          <mxGeometry x="100" y="1200" width="700" height="30" as="geometry" />
        </mxCell>

        <!-- ================= EDGES / ARROWS ================= -->
        <!-- Start -> Targets -->
        <mxCell id="e_start_sup" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="start" target="s_weather" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Targets -> Weather -->
        <mxCell id="e_s1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="s_targets" target="s_weather" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Weather -> Sensors -->
        <mxCell id="e_s2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="s_weather" target="s_sensors" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Sensors -> Dispatch Box -->
        <mxCell id="e_sensors_disp" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="s_sensors" target="dispatch_box" parent="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="700" y="259" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- Dispatch Box -> Delay Augmentation -->
        <mxCell id="e_disp_delay" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="dispatch_box" target="be_delay" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Delay -> State -->
        <mxCell id="e_delay_state" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="be_delay" target="be_state" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- State -> Heterogeneous Pipeline (PINN) -->
        <mxCell id="e_state_pinn" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="be_state" target="m_pinn" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- PM -> PINN -->
        <mxCell id="e_pm_pinn" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="m_pm" target="m_pinn" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- PINN -> DARE -->
        <mxCell id="e_pinn_dare" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="m_pinn" target="m_dare" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Models -> NMPC OCP -->
        <mxCell id="e_m_nmpc" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="m_pinn" target="be_nmpc" parent="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="450" y="600" />
              <mxPoint x="450" y="600" />
            </Array>
          </mxGeometry>
        </mxCell>

        <!-- NMPC -> Extract Commands -->
        <mxCell id="e_nmpc_opt" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="be_nmpc" target="be_opt" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Optimal Commands -> Blockchain Tokenisation -->
        <mxCell id="e_opt_chain" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="be_opt" target="be_chain" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Blockchain -> Signal Clamping -->
        <mxCell id="e_chain_sig" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="be_chain" target="be_sig" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Signal Generation -> Glasshouse Actuators -->
        <mxCell id="e_sig_act" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="be_sig" target="gh_plant" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Glasshouse internal: Actuators -> Plant -->
        <mxCell id="e_gh1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="gh_act" target="gh_plant" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Glasshouse internal: Plant -> Feedback -->
        <mxCell id="e_gh2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" source="gh_plant" target="gh_feedback" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Glasshouse -> Decision -->
        <mxCell id="e_gh_dec" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" source="gh_plant" target="dec_loop" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Decision -> End (No) -->
        <mxCell id="e_dec_no" value="No" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontFamily=Helvetica;fontSize=12;" edge="1" source="dec_loop" target="end" parent="1">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Decision -> Telemetry Loop (Yes, next step k+1) -->
        <mxCell id="e_dec_yes" value="Yes (k ← k+1)" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.5;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;fontFamily=Helvetica;fontSize=12;" edge="1" source="dec_loop" target="s_sensors" parent="1">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="870" y="1073" />
              <mxPoint x="870" y="159" />
            </Array>
          </mxGeometry>
        </mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''
    with open('fig1_greenhouse_nmpc_pinn_architecture.drawio', 'w', encoding='utf-8') as f:
        f.write(xml_content.strip())
    print("Created fig1_greenhouse_nmpc_pinn_architecture.drawio successfully!")

if __name__ == '__main__':
    create_crop_disease_drawio()
    create_greenhouse_nmpc_pinn_drawio()
