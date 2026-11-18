import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon
import os

def render_diagram(mode="crop", output_prefix="fig1_architecture"):
    """
    Renders the multi-tier flowchart architecture in exact style of the uploaded reference image.
    mode: "crop" for the crop disease framework, "greenhouse" for the NMPC+PINN control framework.
    """
    fig = plt.figure(figsize=(10, 14), dpi=300)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 140)
    ax.axis('off')

    # Font setup
    font_family = 'DejaVu Sans'
    
    # Helper to draw stadium (Start/End)
    def draw_stadium(x, y, w, h, text):
        box = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={h/2}",
                             ec="black", fc="white", lw=1.5, zorder=3)
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2, text, ha='center', va='center',
                fontsize=11, fontweight='bold', fontfamily=font_family, zorder=4)

    # Helper to draw process rectangle
    def draw_box(x, y, w, h, title, subtitle=None, bold_title=True):
        box = Rectangle((x, y), w, h, ec="black", fc="white", lw=1.4, zorder=3)
        ax.add_patch(box)
        if subtitle:
            ax.text(x + w/2, y + h*0.62, title, ha='center', va='center',
                    fontsize=9.5, fontweight='bold' if bold_title else 'normal', fontfamily=font_family, zorder=4)
            ax.text(x + w/2, y + h*0.30, subtitle, ha='center', va='center',
                    fontsize=8.0, color="#222222", fontfamily=font_family, zorder=4)
        else:
            ax.text(x + w/2, y + h/2, title, ha='center', va='center',
                    fontsize=9.5, fontweight='bold' if bold_title else 'normal', fontfamily=font_family, zorder=4)

    # Helper to draw dashed container
    def draw_container(x, y, w, h, label):
        c = Rectangle((x, y), w, h, ec="black", fc="none", lw=1.3, ls=(0, (5, 3)), zorder=1)
        ax.add_patch(c)
        ax.text(x + w/2, y + h - 2.5, label, ha='center', va='top',
                fontsize=10.5, fontweight='bold', fontfamily=font_family, zorder=2)

    # Helper to draw decision diamond
    def draw_diamond(cx, cy, w, h, text):
        half_w = w / 2
        half_h = h / 2
        pts = [[cx, cy + half_h], [cx + half_w, cy], [cx, cy - half_h], [cx - half_w, cy]]
        poly = Polygon(pts, ec="black", fc="white", lw=1.4, zorder=3)
        ax.add_patch(poly)
        ax.text(cx, cy, text, ha='center', va='center',
                fontsize=9.5, fontweight='bold', fontfamily=font_family, zorder=4)

    # Helper to draw orthogonal arrow
    def draw_arrow(start_pt, end_pt, text=None, text_offset=(0, 0)):
        ax.annotate('', xy=end_pt, xytext=start_pt,
                    arrowprops=dict(arrowstyle="-|>", color="black", lw=1.4, mutation_scale=12),
                    zorder=2)
        if text:
            mid_x = (start_pt[0] + end_pt[0]) / 2 + text_offset[0]
            mid_y = (start_pt[1] + end_pt[1]) / 2 + text_offset[1]
            ax.text(mid_x, mid_y, text, ha='center', va='center',
                    fontsize=9, fontweight='bold', fontfamily=font_family,
                    bbox=dict(boxstyle="square,pad=0.1", fc="white", ec="none"), zorder=5)

    if mode == "crop":
        # 1. Start
        draw_stadium(42.5, 131, 15, 3.5, "Start")

        # 2. Container 1: UI
        draw_container(6, 114, 88, 14, "User Interface (Mobile / Web)")
        draw_box(9, 117, 24, 6, "Open Application")
        draw_box(38, 117, 24, 6, "Select Language")
        draw_box(67, 117, 24, 6, "Upload Leaf Image")

        # Arrows inside UI
        draw_arrow((50, 131), (50, 128)) # Start -> UI
        draw_arrow((33, 120), (38, 120))
        draw_arrow((62, 120), (67, 120))

        # Transition Box
        draw_box(35, 102, 30, 6, "Send Image + Request", "HTTP POST (multipart/form-data)")
        
        # Arrow UI Upload -> Transition
        ax.plot([79, 79], [117, 105], color="black", lw=1.4, zorder=2)
        draw_arrow((79, 105), (65, 105))

        # 3. Container 2: Backend Server
        draw_container(6, 36, 88, 62, "Backend Server (FastAPI - Port 8000)")
        draw_arrow((50, 102), (50, 93))

        draw_box(38, 88.5, 24, 4.5, "Request Handler")
        draw_arrow((50, 88.5), (50, 84))

        draw_box(36, 78, 28, 6, "Image Preprocessing", "(Resize, Normalization)")
        draw_arrow((50, 78), (50, 72))

        # Sub-container: Models
        draw_container(8, 57.5, 84, 14.5, "Heterogeneous AI Models (Sequential Inference)")
        draw_box(10, 60.5, 24, 6.5, "YOLOv8n", "(Disease Detection)")
        draw_box(38, 60.5, 24, 6.5, "ResNet-18", "(Classification)")
        draw_box(66, 60.5, 24, 6.5, "Vision Transformer", "(Classification)")

        draw_arrow((34, 63.75), (38, 63.75))
        draw_arrow((62, 63.75), (66, 63.75))

        # Down from models
        draw_arrow((50, 60.5), (50, 55.5))

        draw_box(20, 49.5, 60, 6, "Ensemble Voting & Confidence Calibration",
                 "(Final Prediction: Disease Class + Confidence + Bounding Box)")
        draw_arrow((50, 49.5), (50, 47.5))

        draw_box(20, 41.5, 60, 6, "Multilingual Advisory Generation",
                 "(Explanation + Treatment & Prevention Advice)")
        draw_arrow((50, 41.5), (50, 39.5))

        # Backend bottom boxes
        draw_box(20, 33.5, 60, 6, "Store Results in Database",
                 "(User uploads, Predictions, Bounding boxes, Chat history, Timestamps)")
        draw_arrow((50, 33.5), (50, 31.5))

        draw_box(20, 25.5, 60, 6, "Generate JSON Response", "(Results + Advice)")

        # 4. Container 3: Results Delivery
        draw_container(6, 8, 88, 14.5, "Results Delivery (Web / Mobile)")
        draw_arrow((50, 25.5), (50, 19.5))

        draw_box(9, 11, 24, 6.5, "Display Detected Disease", "(with Bounding Box)")
        draw_box(38, 11, 24, 6.5, "Show Confidence Score", "and Treatment Advice")
        draw_box(67, 11, 24, 6.5, "Chatbot Interaction", "(Multilingual)")

        draw_arrow((33, 14.25), (38, 14.25))
        draw_arrow((62, 14.25), (67, 14.25))

        # 5. Decision & End
        draw_arrow((50, 11), (50, 6)) # Down from delivery
        draw_diamond(50, 3, 26, 5, "Upload Another Image?")

        # Loop Yes: Right -> Up -> into Upload Leaf Image
        ax.plot([63, 97], [3, 3], color="black", lw=1.4, zorder=2)
        ax.plot([97, 97], [3, 120], color="black", lw=1.4, zorder=2)
        draw_arrow((97, 120), (91, 120), text="Yes", text_offset=(-22, -114))

        # Loop No: Down to End
        # Adjusting layout for End oval
        draw_stadium(43, -4, 14, 3.2, "End")
        draw_arrow((50, 0.5), (50, -0.8), text="No", text_offset=(3.5, 0.5))

        # Caption
        fig.text(0.5, 0.015, "Figure 1. Overall architecture of the proposed framework.",
                 ha='center', va='bottom', fontsize=12, fontfamily="Times New Roman")

    else: # Greenhouse Control Architecture
        # 1. Start
        draw_stadium(41, 131, 18, 3.5, "Start (Control Step k)")

        # 2. Container 1: Supervisory & Telemetry
        draw_container(6, 114, 88, 14, "Supervisory & Sensor Acquisition Layer (Sampling Ts = 60 s)")
        draw_box(9, 117, 24, 6, "Agronomic Setpoints", "(Diurnal Temp, RH, CO₂, VPD)")
        draw_box(38, 117, 24, 6, "Weather Forecast d(k)", "(Solar Radiation, Ambient Temp)")
        draw_box(67, 117, 24, 6, "Atmospheric Sensors", "(T_air, W_air, C_CO2 Telemetry)")

        # Arrows inside UI
        draw_arrow((50, 131), (50, 128))
        draw_arrow((33, 120), (38, 120))
        draw_arrow((62, 120), (67, 120))

        # Transition Box
        draw_box(34, 102, 32, 6, "Transmit State & Disturbance Vector", "Synchronous Edge Bus (MQTT / Modbus-TCP)")
        
        # Arrow Sensors -> Transition
        ax.plot([79, 79], [117, 105], color="black", lw=1.4, zorder=2)
        draw_arrow((79, 105), (66, 105))

        # 3. Container 2: Edge Controller
        draw_container(6, 36, 88, 62, "Edge Controller: Delay-Compensated NMPC & Observer Pipeline")
        draw_arrow((50, 102), (50, 93))

        draw_box(22, 88.5, 56, 4.5, "Actuator Transport Delay Augmentation", "(1st-Order Padé Filters: Heat 60s, Vents 30s, Fog 10s, CO₂ 20s)")
        draw_arrow((50, 88.5), (50, 84))

        draw_box(22, 78, 56, 6, "8-State Augmented Microclimate Reconstruction",
                 "x(k) = [T_air, W, C_CO2, T_leaf, x_d,heat, x_d,vent, x_d,fog, x_d,co2]^T")
        draw_arrow((50, 78), (50, 72))

        # Sub-container: Virtual Sensing & Stability
        draw_container(8, 57.5, 84, 14.5, "Heterogeneous Virtual Sensing & Stability Engines")
        draw_box(10, 60.5, 24, 6.5, "Penman-Monteith", "Thermodynamics Loss")
        draw_box(38, 60.5, 24, 6.5, "PINN Canopy Observer", "Estimates T_leaf & Transpiration")
        draw_box(66, 60.5, 24, 6.5, "DARE Stability Engine", "Terminal Cost Matrix P (ρ < 1.0)")

        draw_arrow((34, 63.75), (38, 63.75))
        draw_arrow((62, 63.75), (66, 63.75))

        # Down from models
        draw_arrow((50, 60.5), (50, 55.5))

        draw_box(18, 49.5, 64, 6, "Constrained Nonlinear Model Predictive Control (NMPC OCP)",
                 "Interior-Point Solver: Min Tracking Error + Energy Cost s.t. Bounds & Rate Limits")
        draw_arrow((50, 49.5), (50, 47.5))

        draw_box(18, 41.5, 64, 6, "Extract Optimal Actuator Sequences u*(k)",
                 "Heating Valve Q_heat, Natural Vents A_v, Fogging Rate q_fog, CO₂ Valve U_co2")
        draw_arrow((50, 41.5), (50, 39.5))

        # Bottom boxes in Edge Controller
        draw_box(18, 33.5, 64, 6, "Decentralized Resource Tokenisation (Ethereum)",
                 "Autonomous Accounting of Verified Energy & Water Savings (GHRC)")
        draw_arrow((50, 33.5), (50, 31.5))

        draw_box(18, 25.5, 64, 6, "Actuator Signal Generation & Rate Clamping",
                 "PWM / 4–20 mA Industrial Control Signals to Field Hardware")

        # 4. Container 3: Physical Environment
        draw_container(6, 8, 88, 14.5, "Physical Glasshouse Environment & Tomato Canopy Dynamics")
        draw_arrow((50, 25.5), (50, 19.5))

        draw_box(9, 11, 24, 6.5, "Physical Actuators", "(Pipes, Motors, Fog, Injector)")
        draw_box(38, 11, 24, 6.5, "Coupled Microclimate Physics", "(Energy, Vapor, CO₂ Balance)")
        draw_box(67, 11, 24, 6.5, "Canopy State Evolution", "T_leaf & Transpiration Response")

        draw_arrow((33, 14.25), (38, 14.25))
        draw_arrow((62, 14.25), (67, 14.25))

        # 5. Decision & End
        draw_arrow((50, 11), (50, 6))
        draw_diamond(50, 3, 28, 5, "Control Step k < K_sim?")

        # Loop Yes
        ax.plot([64, 97], [3, 3], color="black", lw=1.4, zorder=2)
        ax.plot([97, 97], [3, 120], color="black", lw=1.4, zorder=2)
        draw_arrow((97, 120), (91, 120), text="Yes (k ← k+1)", text_offset=(-22, -114))

        # Loop No
        draw_stadium(41, -4, 18, 3.2, "End (Sim Complete)")
        draw_arrow((50, 0.5), (50, -0.8), text="No", text_offset=(3.5, 0.5))

        # Caption
        fig.text(0.5, 0.015, "Figure 1. Overall architecture of the proposed delay-compensated NMPC and PINN framework.",
                 ha='center', va='bottom', fontsize=12, fontfamily="Times New Roman")

    ax.set_ylim(-6, 137)
    plt.tight_layout()
    plt.savefig(f"{output_prefix}.png", dpi=300, bbox_inches='tight')
    plt.savefig(f"{output_prefix}.pdf", bbox_inches='tight')
    plt.close()
    print(f"Rendered {output_prefix}.png and {output_prefix}.pdf successfully!")

if __name__ == '__main__':
    # 1. Render the crop disease diagram
    render_diagram(mode="crop", output_prefix="fig1_crop_disease_architecture")
    # 2. Render the greenhouse NMPC+PINN diagram
    render_diagram(mode="greenhouse", output_prefix="fig1_greenhouse_nmpc_pinn_architecture")
    # 3. Also update the project's fig1_system_architecture files
    render_diagram(mode="greenhouse", output_prefix="fig1_system_architecture")
