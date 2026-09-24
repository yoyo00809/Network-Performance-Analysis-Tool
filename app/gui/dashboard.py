# ==========================================
# Network Performance Analysis Tool (NPAT)
# GUI Dashboard
# ==========================================

import os
import threading
import tkinter as tk
from tkinter import messagebox, ttk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from app.monitoring.monitor import monitor_once

from app.network.scanner import (
    get_local_network,
    scan_network,
)

from app.database.database import (
    create_database,
    get_test_history,
)

from app.analysis.trend_analysis import (
    analyze_historical_tests,
    get_metric_series,
)

from app.reports.report_generator import (
    generate_text_report,
    save_text_report,
)

from app.reports.export import (
    export_report_to_csv,
)


# ==========================================
# Main Dashboard
# ==========================================

class NPATDashboard:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Network Performance Analysis Tool - NPAT"
        )

        self.root.geometry(
            "1200x850"
        )

        self.root.minsize(
            1100,
            700
        )
        
        # ----------------------------------
        # Scrollable Main Dashboard
        # ----------------------------------

        self.main_canvas = tk.Canvas(
            self.root,
            highlightthickness=0
        )

        self.main_scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.main_canvas.yview
        )

        self.main_canvas.configure(
            yscrollcommand=self.main_scrollbar.set
        )

        self.main_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.main_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.main_content = tk.Frame(
            self.main_canvas
        )

        self.main_canvas_window = self.main_canvas.create_window(
            (0, 0),
            window=self.main_content,
            anchor="nw"
)       

        def update_main_scroll_region(event=None):

            self.main_canvas.configure(
                scrollregion=self.main_canvas.bbox("all")
            )

        self.main_content.bind(
            "<Configure>",
            update_main_scroll_region
        )

        def resize_main_content(event):

            self.main_canvas.itemconfigure(
                self.main_canvas_window,
                width=event.width
            )

        self.main_canvas.bind(
            "<Configure>",
            resize_main_content
        )

        def main_mousewheel(event):

            self.main_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        self.main_canvas.bind_all(
            "<MouseWheel>",
            main_mousewheel
        )
        

        # ----------------------------------
        # Variables
        # ----------------------------------

        self.host_var = tk.StringVar()

        self.status_var = tk.StringVar(
            value="Ready"
        )
        
        # ----------------------------------
        # Network Scanner Variables
        # ----------------------------------

        self.scanner_network_var = tk.StringVar(
            value="Detecting..."
        )

        self.scanner_status_var = tk.StringVar(
            value="Ready"
        )

        self.scanner_count_var = tk.StringVar(
            value="0 devices found"
        )

        self.latency_var = tk.StringVar(
            value="-- ms"
            )
        self.jitter_var = tk.StringVar(
            value="-- ms"
            )
        self.packet_loss_var = tk.StringVar(
            value="-- %"
            )
        
        self.download_speed_var = tk.StringVar(
            value="-- Mbps"
            )
        
        self.upload_speed_var = tk.StringVar(
            value="-- Mbps"
            )
        
        self.overall_var = tk.StringVar(
            value="--"
            )
        
        self.health_score_var = tk.StringVar(
            value="-- / 100"
            )

        self.health_status_var = tk.StringVar(
            value="--"
        )

        self.anomaly_status_var = tk.StringVar(
            value="--"
        )

        self.anomaly_count_var = tk.StringVar(
            value="--"
        )

        self.anomaly_severity_var = tk.StringVar(
            value="--"
        )

        # ----------------------------------
        # Build Interface
        # ----------------------------------

        self.create_header()
        self.create_input_section()
        self.create_network_scanner_section()
        self.create_metrics_section()
        self.create_bottom_buttons()
        self.create_chart_section()
        self.create_analysis_section()
        self.create_anomaly_section()
        self.create_recommendations_section()

    # ======================================
    # Header
    # ======================================

    def create_header(self):

        header = tk.Frame(
            self.main_content,
            bg="#1f2937",
            height=90
        )

        header.pack(
            fill="x"
        )

        title = tk.Label(
            header,
            text="NETWORK PERFORMANCE ANALYSIS TOOL",
            font=("Arial", 22, "bold"),
            bg="#1f2937",
            fg="white"
        )

        title.pack(
            pady=(15, 2)
        )

        subtitle = tk.Label(
            header,
            text="NPAT - Network Monitoring & Analysis Dashboard",
            font=("Arial", 11),
            bg="#1f2937",
            fg="white"
        )

        subtitle.pack()

    # ======================================
    # Input Section
    # ======================================

    def create_input_section(self):

        section = tk.Frame(
            self.main_content,
            padx=25,
            pady=15
        )

        section.pack(
            fill="x"
        )

        label = tk.Label(
            section,
            text="Target Host / IP Address:",
            font=("Arial", 12, "bold")
        )

        label.pack(
            side="left"
        )

        self.host_entry = tk.Entry(
            section,
            textvariable=self.host_var,
            font=("Arial", 12),
            width=30
        )

        self.host_entry.pack(
            side="left",
            padx=10
        )

        self.host_entry.insert(
            0,
            "google.com"
        )

        self.test_button = tk.Button(
            section,
            text="START NETWORK TEST",
            font=("Arial", 11, "bold"),
            command=self.start_test,
            padx=15,
            pady=8
        )

        self.test_button.pack(
            side="left"
        )

        status_label = tk.Label(
            section,
            textvariable=self.status_var,
            font=("Arial", 10)
        )

        status_label.pack(
            side="left",
            padx=15
        )

    
    # ======================================
    # Network Scanner
    # ======================================

    def create_network_scanner_section(self):

        section = tk.LabelFrame(
            self.main_content,
            text="Network Scanner",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10
        )

        section.pack(
            fill="x",
            padx=25,
            pady=8
        )

        # ----------------------------------
        # Network Information
        # ----------------------------------

        info_frame = tk.Frame(
            section
        )

        info_frame.pack(
            fill="x",
            pady=(0, 8)
        )

        network_label = tk.Label(
            info_frame,
            text="Local Network:",
            font=("Arial", 10, "bold")
        )

        network_label.pack(
            side="left"
        )

        network_value = tk.Label(
            info_frame,
            textvariable=self.scanner_network_var,
            font=("Arial", 10)
        )

        network_value.pack(
            side="left",
            padx=8
        )

        status_label = tk.Label(
            info_frame,
            textvariable=self.scanner_status_var,
            font=("Arial", 10)
        )

        status_label.pack(
            side="left",
            padx=20
        )

        count_label = tk.Label(
            info_frame,
            textvariable=self.scanner_count_var,
            font=("Arial", 10, "bold")
        )

        count_label.pack(
            side="right"
        )

        # ----------------------------------
        # Scanner Buttons
        # ----------------------------------

        button_frame = tk.Frame(
            section
        )

        button_frame.pack(
            fill="x",
            pady=(0, 8)
        )

        self.scan_button = tk.Button(
            button_frame,
            text="SCAN NETWORK",
            font=("Arial", 10, "bold"),
            command=self.start_network_scan,
            padx=15,
            pady=7
        )

        self.scan_button.pack(
            side="left"
        )

        clear_button = tk.Button(
            button_frame,
            text="CLEAR RESULTS",
            font=("Arial", 10, "bold"),
            command=self.clear_network_scan,
            padx=15,
            pady=7
        )

        clear_button.pack(
            side="left",
            padx=8
        )

        # ----------------------------------
        # Device Table
        # ----------------------------------

        table_frame = tk.Frame(
            section
        )

        table_frame.pack(
            fill="x"
        )

        columns = (
            "ip_address",
            "status"
        )

        self.scanner_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=5
        )

        self.scanner_tree.heading(
            "ip_address",
            text="IP Address"
        )

        self.scanner_tree.heading(
            "status",
            text="Status"
        )

        self.scanner_tree.column(
            "ip_address",
            width=250,
            anchor="center"
        )

        self.scanner_tree.column(
            "status",
            width=180,
            anchor="center"
        )

        scanner_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.scanner_tree.yview
        )

        self.scanner_tree.configure(
            yscrollcommand=scanner_scrollbar.set
        )

        self.scanner_tree.pack(
            side="left",
            fill="x",
            expand=True
        )

        scanner_scrollbar.pack(
            side="right",
            fill="y"
        )

        # ----------------------------------
        # Detect Local Network
        # ----------------------------------

        try:

            network = get_local_network()

            if network is not None:
                self.scanner_network_var.set(
                    str(network)
                )
            else:
                self.scanner_network_var.set(
                    "Unable to detect"
                )

        except Exception:
            self.scanner_network_var.set(
                "Unable to detect"
            )

    # ======================================
    # Start Network Scan
    # ======================================

    def start_network_scan(self):

        if getattr(
            self,
            "_network_scan_running",
            False
        ):
            return

        self._network_scan_running = True

        self.scan_button.config(
            state="disabled"
        )

        self.scanner_status_var.set(
            "Scanning network..."
        )

        self.scanner_count_var.set(
            "Scanning..."
        )

        self.clear_network_scan(
            keep_status=True
        )

        scan_thread = threading.Thread(
            target=self._run_network_scan,
            daemon=True
        )

        scan_thread.start()

    # ======================================
    # Background Network Scan
    # ======================================

    def _run_network_scan(self):

        try:

            network = get_local_network()

            if network is None:

                self.root.after(
                    0,
                    lambda: self._network_scan_finished(
                        [],
                        "Unable to detect local network"
                    )
                )

                return

            active_devices = scan_network(
                network
            )

            self.root.after(
                0,
                lambda: self._network_scan_finished(
                    active_devices,
                    "Scan completed"
                )
            )

        except Exception as error:

            self.root.after(
                0,
                lambda: self._network_scan_finished(
                    [],
                    f"Scan failed: {error}"
                )
            )

    # ======================================
    # Network Scan Completion
    # ======================================

    def _network_scan_finished(
        self,
        active_devices,
        status_message
    ):

        self._network_scan_running = False

        self.scan_button.config(
            state="normal"
        )

        self.scanner_status_var.set(
            status_message
        )

        self.scanner_count_var.set(
            f"{len(active_devices)} devices found"
        )

        for ip_address in active_devices:

            self.scanner_tree.insert(
                "",
                tk.END,
                values=(
                    ip_address,
                    "Active"
                )
            )

    # ======================================
    # Clear Network Scan
    # ======================================

    def clear_network_scan(
        self,
        keep_status=False
    ):

        if hasattr(
            self,
            "scanner_tree"
        ):

            for item in self.scanner_tree.get_children():

                self.scanner_tree.delete(
                    item
                )

        if not keep_status:

            self.scanner_status_var.set(
                "Ready"
            )

            self.scanner_count_var.set(
                "0 devices found"
            )
    
    
    # ======================================
    # Metrics Section
    # ======================================

    def create_metrics_section(self):

        section = tk.Frame(
            self.main_content,
            padx=20,
            pady=5
        )

        section.pack(
            fill="x"
        )

        self.create_metric_card(
            section,
            "LATENCY",
            self.latency_var
        ).pack(
            side="left",
            expand=True,
            fill="both",
            padx=5
        )

        self.create_metric_card(
            section,
            "JITTER",
            self.jitter_var
        ).pack(
            side="left",
            expand=True,
            fill="both",
            padx=5
        )

        self.create_metric_card(
            section,
            "PACKET LOSS",
            self.packet_loss_var
        ).pack(
            side="left",
            expand=True,
            fill="both",
            padx=5
        )
        
        self.create_metric_card(
            section,
            "DOWNLOAD SPEED",
            self.download_speed_var
            ).pack(
                side="left",
                expand=True,
                fill="both",
                padx=5
            )

        self.create_metric_card(
            section,
            "UPLOAD SPEED",
            self.upload_speed_var
        ).pack(
            side="left",
            expand=True,
            fill="both",
            padx=5
        )

        self.create_metric_card(
            section,
            "OVERALL STATUS",
            self.overall_var
        ).pack(
            side="left",
            expand=True,
            fill="both",
            padx=5
        )

        self.create_metric_card(
            section,
            "NETWORK HEALTH",
            self.health_score_var
        ).pack(
            side="left",
            expand=True,
            fill="both",
            padx=5
        )

    # ======================================
    # Metric Card
    # ======================================

    def create_metric_card(
        self,
        parent,
        title,
        variable
    ):

        card = tk.Frame(
            parent,
            relief="ridge",
            borderwidth=2,
            padx=10,
            pady=12
        )

        title_label = tk.Label(
            card,
            text=title,
            font=("Arial", 10, "bold")
        )

        title_label.pack()

        value_label = tk.Label(
            card,
            textvariable=variable,
            font=("Arial", 18, "bold")
        )

        value_label.pack(
            pady=(6, 0)
        )

        return card

    # ======================================
    # Bottom Buttons
    # ======================================

    def create_bottom_buttons(self):

        section = tk.Frame(
            self.main_content,
            padx=25,
            pady=5
        )

        section.pack(
            fill="x"
        )

        history_button = tk.Button(
            section,
            text="VIEW TEST HISTORY",
            font=("Arial", 10, "bold"),
            command=self.show_history,
            padx=15,
            pady=7
        )

        history_button.pack(
            side="left",
            padx=5
        )

        txt_button = tk.Button(
            section,
            text="OPEN TXT REPORT",
            font=("Arial", 10, "bold"),
            command=self.open_text_report,
            padx=15,
            pady=7
        )

        txt_button.pack(
            side="left",
            padx=5
        )

        csv_button = tk.Button(
            section,
            text="OPEN CSV REPORT",
            font=("Arial", 10, "bold"),
            command=self.open_csv_report,
            padx=15,
            pady=7
        )

        csv_button.pack(
            side="left",
            padx=5
        )

        # ----------------------------------
        # Historical Trends Button
        # ----------------------------------

        trend_button = tk.Button(
            section,
            text="HISTORICAL TRENDS",
            font=("Arial", 10, "bold"),
            command=self.show_historical_trends,
            padx=15,
            pady=7
        )

        trend_button.pack(
            side="left",
            padx=5
        )

    # ======================================
    # Performance Chart
    # ======================================

    def create_chart_section(self):

        section = tk.LabelFrame(
            self.main_content,
            text="Ping Response Time",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=5
        )

        section.pack(
            fill="x",
            expand=False,
            padx=25,
            pady=8
        )

        section.configure(
            height=250
        )

        section.pack_propagate(
            False
        )

        self.figure = Figure(
            figsize=(8, 2.4),
            dpi=100
        )

        self.ax = self.figure.add_subplot(
            111
        )

        self.ax.set_title(
            "Ping Response Time"
        )

        self.ax.set_xlabel(
            "Ping Number"
        )

        self.ax.set_ylabel(
            "Response Time (ms)"
        )

        self.ax.grid(
            True
        )

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=section
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # ======================================
    # Update Chart
    # ======================================

    def update_chart(
        self,
        response_times
    ):

        self.ax.clear()

        if response_times:

            ping_numbers = list(
                range(
                    1,
                    len(response_times) + 1
                )
            )

            self.ax.plot(
                ping_numbers,
                response_times,
                marker="o",
                linewidth=2
            )

            self.ax.set_title(
                "Ping Response Time"
            )

            self.ax.set_xlabel(
                "Ping Number"
            )

            self.ax.set_ylabel(
                "Response Time (ms)"
            )

            self.ax.grid(
                True
            )

            self.ax.set_xticks(
                ping_numbers
            )

        else:

            self.ax.set_title(
                "No Response Data Available"
            )

            self.ax.set_xlabel(
                "Ping Number"
            )

            self.ax.set_ylabel(
                "Response Time (ms)"
            )

            self.ax.grid(
                True
            )

        self.figure.tight_layout()

        self.canvas.draw()

    # ======================================
    # Analysis Section
    # ======================================

    def create_analysis_section(self):

        section = tk.LabelFrame(
            self.main_content,
            text="Performance Analysis",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8
        )

        section.pack(
            fill="x",
            padx=25,
            pady=5
        )

        self.analysis_text = tk.Label(
            section,
            text=(
                "Latency Status : --\n"
                "Jitter Status  : --\n"
                "Packet Loss    : --\n"
                "Health Score   : -- / 100\n"
                "Health Status  : --"
            ),
            font=("Arial", 11),
            justify="left",
            anchor="w"
        )

        self.analysis_text.pack(
            fill="x"
        )

    # ======================================
    # Anomaly Detection Section
    # ======================================

    def create_anomaly_section(self):

        section = tk.LabelFrame(
            self.main_content,
            text="Anomaly Detection",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8
        )

        section.pack(
            fill="x",
            padx=25,
            pady=5
        )

        self.anomaly_text = tk.Label(
            section,
            text=(
                "Anomaly Status : --\n"
                "Anomaly Count  : --\n"
                "Severity       : --\n"
                "Types          : --\n"
                "Details        : --"
            ),
            font=("Arial", 10),
            justify="left",
            anchor="w"
        )

        self.anomaly_text.pack(
            fill="x"
        )

    # ======================================
    # Recommendations Section
    # ======================================

    def create_recommendations_section(self):

        section = tk.LabelFrame(
            self.main_content,
            text="Recommendations",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=8
        )

        section.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(5, 10)
        )

        self.recommendations_text = tk.Text(
            section,
            height=5,
            font=("Arial", 10),
            wrap="word"
        )

        self.recommendations_text.pack(
            fill="both",
            expand=True
        )

        self.recommendations_text.insert(
            "1.0",
            "Run a network test to view recommendations."
        )

        self.recommendations_text.config(
            state="disabled"
        )

    # ======================================
    # Start Test
    # ======================================

    def start_test(self):

        host = self.host_var.get().strip()

        if not host:

            messagebox.showwarning(
                "Input Required",
                "Please enter a hostname or IP address."
            )

            return

        self.test_button.config(
            state="disabled",
            text="TESTING..."
        )

        self.status_var.set(
            f"Testing {host}..."
        )

        thread = threading.Thread(
            target=self.run_test,
            args=(host,),
            daemon=True
        )

        thread.start()

    # ======================================
    # Run Test
    # ======================================

    def run_test(self, host):

        try:

            result = monitor_once(
                host,
                count=4,
                include_bandwidth=True
            )

            self.root.after(
                0,
                lambda: self.display_results(
                    result
                )
            )

        except Exception as error:

            self.root.after(
                0,
                lambda: self.show_error(
                    str(error)
                )
            )

    # ======================================
    # Display Results
    # ======================================

    def display_results(self, result):

        metrics = result["metrics"]

        analysis = result["analysis"]

        health_score = result["health_score"]
        
        bandwidth = result.get(
            "bandwidth",
            {}
        )

        download_speed = bandwidth.get(
            "download_speed_mbps"
        )

        upload_speed = bandwidth.get(
            "upload_speed_mbps"
        )

        anomaly = result.get(
            "anomaly",
            {}
        )

        recommendations = result["recommendations"]

        ping_result = result["ping"]

        # ----------------------------------
        # Generate Latest Reports
        # ----------------------------------

        reports_directory = os.path.join(
            "data",
            "reports"
        )

        os.makedirs(
            reports_directory,
            exist_ok=True
        )
        
        bandwidth = result.get(
            "bandwidth",
            {}
        )

        report = generate_text_report(
            result["host"],
            ping_result,
            metrics,
            analysis,
            recommendations,
            bandwidth
        )

        text_report_path = os.path.join(
            reports_directory,
            "network_report.txt"
        )

        csv_report_path = os.path.join(
            reports_directory,
            "network_report.csv"
        )

        save_text_report(
            report,
            text_report_path
        )

        export_report_to_csv(
            csv_report_path,
            result["host"],
            ping_result,
            metrics,
            analysis,
            bandwidth
        )

        # ----------------------------------
        # Metrics
        # ----------------------------------

        self.latency_var.set(
            f"{metrics['latency_average']} ms"
        )

        self.jitter_var.set(
            f"{metrics['jitter']} ms"
        )

        self.packet_loss_var.set(
            f"{metrics['packet_loss']}%"
        )
        
        
        # ----------------------------------
        # Bandwidth
        # ----------------------------------

        bandwidth = result.get(
            "bandwidth",
            {}
        )

        download_speed = bandwidth.get(
            "download_speed_mbps"
        )

        upload_speed = bandwidth.get(
            "upload_speed_mbps"
        )

        if download_speed is not None:
            self.download_speed_var.set(
                f"{download_speed:.2f} Mbps"
            )
        else:
            self.download_speed_var.set(
                "-- Mbps"
            )

        if upload_speed is not None:
            self.upload_speed_var.set(
                f"{upload_speed:.2f} Mbps"
            )
        else:
            self.upload_speed_var.set(
                "-- Mbps"
            )

        self.overall_var.set(
            analysis["overall_status"]
        )

        # ----------------------------------
        # Network Health
        # ----------------------------------

        if health_score["health_score"] is not None:

            self.health_score_var.set(
                f"{health_score['health_score']} / 100"
            )

            self.health_status_var.set(
                health_score["health_status"]
            )

        else:

            self.health_score_var.set(
                "-- / 100"
            )

            self.health_status_var.set(
                "Unavailable"
            )

        # ----------------------------------
        # Update Graph
        # ----------------------------------

        self.update_chart(
            ping_result["response_times"]
        )

        # ----------------------------------
        # Analysis
        # ----------------------------------

        self.analysis_text.config(
            text=(
                f"Latency Status : "
                f"{analysis['latency_status']}\n"
                f"Jitter Status  : "
                f"{analysis['jitter_status']}\n"
                f"Packet Loss    : "
                f"{analysis['packet_loss_status']}\n"
                f"Health Score   : "
                f"{health_score['health_score']} / 100\n"
                f"Health Status  : "
                f"{health_score['health_status']}"
            )
        )

        # ----------------------------------
        # Anomaly Detection
        # ----------------------------------

        anomaly_detected = anomaly.get(
            "anomaly_detected",
            False
        )

        anomaly_count = anomaly.get(
            "anomaly_count",
            0
        )

        anomaly_severity = anomaly.get(
            "severity",
            "Normal"
        )

        anomaly_types = anomaly.get(
            "anomaly_types",
            []
        )

        anomaly_details = anomaly.get(
            "details",
            []
        )

        if anomaly_types:

            anomaly_types_display = ", ".join(
                anomaly_types
            )

        else:

            anomaly_types_display = "None"

        if anomaly_details:

            anomaly_details_display = "\n".join(
                f"• {detail}"
                for detail in anomaly_details
            )

        else:

            anomaly_details_display = (
                "No anomalies detected."
            )

        if anomaly_detected:

            anomaly_status_display = "DETECTED"

        else:

            anomaly_status_display = "Normal"

        self.anomaly_status_var.set(
            anomaly_status_display
        )

        self.anomaly_count_var.set(
            str(anomaly_count)
        )

        self.anomaly_severity_var.set(
            anomaly_severity
        )

        self.anomaly_text.config(
            text=(
                f"Anomaly Status : "
                f"{anomaly_status_display}\n"
                f"Anomaly Count  : "
                f"{anomaly_count}\n"
                f"Severity       : "
                f"{anomaly_severity}\n"
                f"Types          : "
                f"{anomaly_types_display}\n"
                f"Details        :\n"
                f"{anomaly_details_display}"
            )
        )

        # ----------------------------------
        # Recommendations
        # ----------------------------------

        self.recommendations_text.config(
            state="normal"
        )

        self.recommendations_text.delete(
            "1.0",
            tk.END
        )

        for index, recommendation in enumerate(
            recommendations,
            start=1
        ):

            self.recommendations_text.insert(
                tk.END,
                f"{index}. {recommendation}\n\n"
            )

        self.recommendations_text.config(
            state="disabled"
        )

        # ----------------------------------
        # Reset Button
        # ----------------------------------

        self.test_button.config(
            state="normal",
            text="START NETWORK TEST"
        )

        self.status_var.set(
            f"Test completed for {result['host']}"
        )

    # ======================================
    # Test History Window
    # ======================================

    def show_history(self):

        try:

            app = create_database()

            with app.app_context():

                history = get_test_history(
                    limit=50
                )

                history_data = []

                for record in history:

                    history_data.append({
                        "id": record.id,
                        "host": record.host,
                        "latency": record.latency_average,
                        "jitter": record.jitter,
                        "packet_loss": record.packet_loss,
                        "download_speed": record.download_speed_mbps,
                        "upload_speed": record.upload_speed_mbps,
                        "health_score": record.health_score,
                        "health_status": record.health_status,
                        "anomaly_detected": record.anomaly_detected,
                        "anomaly_count": record.anomaly_count,
                        "anomaly_severity": record.anomaly_severity,
                        "status": record.overall_status,
                        "created_at": record.created_at,
                    })

        except Exception as error:

            messagebox.showerror(
                "History Error",
                f"Unable to load test history:\n\n{error}"
            )

            return

        # ----------------------------------
        # Create History Window
        # ----------------------------------

        history_window = tk.Toplevel(
            self.root
        )

        history_window.title(
            "NPAT - Test History"
        )

        history_window.geometry(
            "1350x500"
        )

        history_window.minsize(
            900,
            400
        )

        # ----------------------------------
        # Heading
        # ----------------------------------

        heading = tk.Label(
            history_window,
            text="NETWORK TEST HISTORY",
            font=("Arial", 18, "bold")
        )

        heading.pack(
            pady=15
        )

        # ----------------------------------
        # Table Frame
        # ----------------------------------

        table_frame = tk.Frame(
            history_window
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "ID",
            "Host",
            "Latency",
            "Jitter",
            "Packet Loss",
            "Download Speed",
            "Upload Speed",
            "Health Score",
            "Health Status",
            "Anomaly",
            "Count",
            "Severity",
            "Status",
            "Created At"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        # ----------------------------------
        # Column Headings
        # ----------------------------------

        tree.heading(
            "ID",
            text="ID"
        )

        tree.heading(
            "Host",
            text="Host"
        )

        tree.heading(
            "Latency",
            text="Latency (ms)"
        )

        tree.heading(
            "Jitter",
            text="Jitter (ms)"
        )

        tree.heading(
            "Packet Loss",
            text="Packet Loss (%)"
        )
        
        tree.heading(
            "Download Speed",
            text="Download (Mbps)"
        )

        tree.heading(
            "Upload Speed",
            text="Upload (Mbps)"
        )

        tree.heading(
            "Health Score",
            text="Health Score"
        )

        tree.heading(
            "Health Status",
            text="Health Status"
        )

        tree.heading(
            "Anomaly",
            text="Anomaly"
        )

        tree.heading(
            "Count",
            text="Count"
        )

        tree.heading(
            "Severity",
            text="Severity"
        )

        tree.heading(
            "Status",
            text="Overall Status"
        )

        tree.heading(
            "Created At",
            text="Created At"
        )

        # ----------------------------------
        # Column Widths
        # ----------------------------------

        tree.column(
            "ID",
            width=50,
            anchor="center"
        )

        tree.column(
            "Host",
            width=150
        )

        tree.column(
            "Latency",
            width=90,
            anchor="center"
        )

        tree.column(
            "Jitter",
            width=90,
            anchor="center"
        )

        tree.column(
            "Packet Loss",
            width=110,
            anchor="center"
        )
        
        tree.column(
            "Download Speed",
            width=120,
            anchor="center"
        )

        tree.column(
            "Upload Speed",
            width=120,
            anchor="center"
        )

        tree.column(
            "Health Score",
            width=110,
            anchor="center"
        )

        tree.column(
            "Health Status",
            width=110,
            anchor="center"
        )

        tree.column(
            "Anomaly",
            width=90,
            anchor="center"
        )

        tree.column(
            "Count",
            width=70,
            anchor="center"
        )

        tree.column(
            "Severity",
            width=100,
            anchor="center"
        )

        tree.column(
            "Status",
            width=110,
            anchor="center"
        )

        tree.column(
            "Created At",
            width=170
        )

        # ----------------------------------
        # Scrollbar
        # ----------------------------------

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(
            yscrollcommand=scrollbar.set
        )

        tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ----------------------------------
        # Insert History
        # ----------------------------------

        for record in history_data:

            health_score = record[
                "health_score"
            ]

            if health_score is not None:

                health_score_display = (
                    f"{health_score} / 100"
                )

            else:

                health_score_display = "--"

            tree.insert(
                "",
                tk.END,
                values=(
                    record["id"],
                    record["host"],
                    record["latency"],
                    record["jitter"],
                    record["packet_loss"],
                    (
                        f"{record['download_speed']:.2f}"
                        if record["download_speed"] is not None
                        else "--"
                    ),
                    (
                        f"{record['upload_speed']:.2f}"
                        if record["upload_speed"] is not None
                        else "--"
                    ),
                    health_score_display,
                    record["health_status"] or "--",
                    (
                        "Detected"
                        if record["anomaly_detected"]
                        else "Normal"
                    ),
                    (
                        record["anomaly_count"]
                        if record["anomaly_count"] is not None
                        else 0
                    ),
                    record["anomaly_severity"] or "--",
                    record["status"],
                    record["created_at"],
                )
            )

        # ----------------------------------
        # Empty History Message
        # ----------------------------------

        if not history_data:

            empty_label = tk.Label(
                history_window,
                text="No network test history available.",
                font=("Arial", 11)
            )

            empty_label.pack(
                pady=5
            )

    # ======================================
    # Historical Trend Analysis
    # ======================================

    def show_historical_trends(self):

        try:

            # ----------------------------------
            # Load Historical Database Records
            # ----------------------------------

            app = create_database()

            with app.app_context():

                history = get_test_history(
                    limit=50
                )

                trend_data = analyze_historical_tests(
                    history
                )

                metric_series = get_metric_series(
                    history
                )

        except Exception as error:

            messagebox.showerror(
                "Historical Trend Error",
                f"Unable to load historical trends:\n\n{error}"
            )

            return

        # ----------------------------------
        # Create Trend Window
        # ----------------------------------

        trend_window = tk.Toplevel(
            self.root
        )

        trend_window.title(
            "NPAT - Historical Trend Analysis"
        )

        trend_window.geometry(
            "1250x850"
        )

        trend_window.minsize(
            1000,
            850
        )

        # ----------------------------------
        # Scrollable Trend Content
        # ----------------------------------

        trend_scroll_canvas = tk.Canvas(
            trend_window,
            highlightthickness=0
        )

        trend_scrollbar = ttk.Scrollbar(
            trend_window,
            orient="vertical",
            command=trend_scroll_canvas.yview
        )

        trend_scroll_canvas.configure(
            yscrollcommand=trend_scrollbar.set
        )

        trend_scrollbar.pack(
            side="right",
            fill="y"
        )

        trend_scroll_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        trend_content = tk.Frame(
            trend_scroll_canvas
        )

        trend_scroll_window = trend_scroll_canvas.create_window(
            (0, 0),
            window=trend_content,
            anchor="nw"
        )

        def update_trend_scroll_region(event=None):

            trend_scroll_canvas.configure(
                scrollregion=trend_scroll_canvas.bbox("all")
            )

        trend_content.bind(
            "<Configure>",
            update_trend_scroll_region
        )

        def resize_trend_content(event):

            trend_scroll_canvas.itemconfigure(
                trend_scroll_window,
                width=event.width
            )

        trend_scroll_canvas.bind(
            "<Configure>",
            resize_trend_content
        )

        def trend_mousewheel(event):

            trend_scroll_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        trend_window.bind(
            "<MouseWheel>",
            trend_mousewheel
        )

        # ----------------------------------
        # Heading
        # ----------------------------------

        heading = tk.Label(
            trend_content,
            text="HISTORICAL TREND ANALYSIS",
            font=("Arial", 20, "bold")
        )

        heading.pack(
            pady=(15, 5)
        )

        subtitle = tk.Label(
            trend_content,
            text=(
                "Analysis of recent network performance "
                "test history"
            ),
            font=("Arial", 10)
        )

        subtitle.pack(
            pady=(0, 10)
        )

        # ----------------------------------
        # Summary Section
        # ----------------------------------

        summary_frame = tk.Frame(
            trend_content,
            padx=15,
            pady=5
        )

        summary_frame.pack(
            fill="x"
        )

        total_tests = trend_data[
            "total_tests"
        ]

        available = trend_data[
            "availability"
        ]["available"]

        unavailable = trend_data[
            "availability"
        ]["unavailable"]

        failure_events = trend_data[
            "failure_events"
        ]

        recovery_events = trend_data[
            "recovery_events"
        ]

        summary_items = [
            (
                "TOTAL TESTS",
                str(total_tests)
            ),
            (
                "AVAILABLE",
                str(available)
            ),
            (
                "UNAVAILABLE",
                str(unavailable)
            ),
            (
                "FAILURES",
                str(failure_events)
            ),
            (
                "RECOVERIES",
                str(recovery_events)
            ),
        ]

        for title, value in summary_items:

            card = tk.Frame(
                summary_frame,
                relief="ridge",
                borderwidth=2,
                padx=15,
                pady=8
            )

            card.pack(
                side="left",
                expand=True,
                fill="both",
                padx=5
            )

            tk.Label(
                card,
                text=title,
                font=("Arial", 9, "bold")
            ).pack()

            tk.Label(
                card,
                text=value,
                font=("Arial", 17, "bold")
            ).pack(
                pady=(4, 0)
            )

        # ----------------------------------
        # Statistics Section
        # ----------------------------------

        statistics_frame = tk.LabelFrame(
            trend_content,
            text="Historical Statistics",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=10
        )

        statistics_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        columns = (
            "Metric",
            "Average",
            "Minimum",
            "Maximum",
            "Samples"
        )

        statistics_tree = ttk.Treeview(
            statistics_frame,
            columns=columns,
            show="headings",
            height=6
        )

        for column in columns:

            statistics_tree.heading(
                column,
                text=column
            )

        statistics_tree.column(
            "Metric",
            width=180,
            anchor="center"
        )

        statistics_tree.column(
            "Average",
            width=150,
            anchor="center"
        )

        statistics_tree.column(
            "Minimum",
            width=150,
            anchor="center"
        )

        statistics_tree.column(
            "Maximum",
            width=150,
            anchor="center"
        )

        statistics_tree.column(
            "Samples",
            width=100,
            anchor="center"
        )

        def format_value(value):

            if value is None:
                return "--"

            return str(value)

        statistics_rows = [
            (
                "Latency (ms)",
                trend_data["latency"]
            ),
            (
                "Jitter (ms)",
                trend_data["jitter"]
            ),
            (
                "Packet Loss (%)",
                trend_data["packet_loss"]
            ),
            (
                "Health Score",
                trend_data["health_score"]
            ),
            (
                "Download Speed (Mbps)",
                trend_data["download_speed"]
            ),
            (
                "Upload Speed (Mbps)",
                trend_data["upload_speed"]
            ),
        ]

        for metric_name, values in statistics_rows:

            statistics_tree.insert(
                "",
                tk.END,
                values=(
                    metric_name,
                    format_value(
                        values["average"]
                    ),
                    format_value(
                        values["minimum"]
                    ),
                    format_value(
                        values["maximum"]
                    ),
                    values["count"]
                )
            )

        statistics_tree.pack(
            fill="x",
            expand=True
        )

        # ----------------------------------
        # Historical Charts
        # ----------------------------------

        chart_frame = tk.LabelFrame(
            trend_content,
            text="Performance Trends",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )

        chart_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=5
        )
        chart_frame.configure(
            height=360
        )

        chart_frame.pack_propagate(False)

        trend_figure = Figure(
            figsize=(10, 3.5),
            dpi=100
        )

        trend_ax = trend_figure.add_subplot(
            111
        )

        latency_series = metric_series[
            "latency"
        ]

        jitter_series = metric_series[
            "jitter"
        ]

        packet_loss_series = metric_series[
            "packet_loss"
        ]

        health_series = metric_series[
            "health_score"
        ]
        
        download_series = metric_series[
            "download_speed"
        ]

        upload_series = metric_series[
            "upload_speed"
        ]

        # Database history is returned newest-first.
        # Reverse it so the chart reads oldest -> newest.

        latency_series = list(
            reversed(latency_series)
        )

        jitter_series = list(
            reversed(jitter_series)
        )

        packet_loss_series = list(
            reversed(packet_loss_series)
        )

        health_series = list(
            reversed(health_series)
        )
        
        download_series = list(
            reversed(download_series)
        )
        
        upload_series = list(
            reversed(upload_series)
        )

        test_numbers = list(
            range(
                1,
                len(history) + 1
            )
        )

        plotted = False

        # ----------------------------------
        # Latency
        # ----------------------------------

        if any(
            value is not None
            for value in latency_series
        ):

            trend_ax.plot(
                test_numbers,
                latency_series,
                marker="o",
                linewidth=2,
                label="Latency (ms)"
            )

            plotted = True

        # ----------------------------------
        # Jitter
        # ----------------------------------

        if any(
            value is not None
            for value in jitter_series
        ):

            trend_ax.plot(
                test_numbers,
                jitter_series,
                marker="o",
                linewidth=2,
                label="Jitter (ms)"
            )

            plotted = True

        # ----------------------------------
        # Packet Loss
        # ----------------------------------

        if any(
            value is not None
            for value in packet_loss_series
        ):

            trend_ax.plot(
                test_numbers,
                packet_loss_series,
                marker="o",
                linewidth=2,
                label="Packet Loss (%)"
            )

            plotted = True

        trend_ax.set_title(
            "Latency, Jitter and Packet Loss Trend"
        )

        trend_ax.set_xlabel(
            "Test Number"
        )

        trend_ax.set_ylabel(
            "Metric Value"
        )

        trend_ax.grid(
            True
        )

        if plotted:

            trend_ax.legend()

        else:

            trend_ax.text(
                0.5,
                0.5,
                "No historical metric data available",
                horizontalalignment="center",
                verticalalignment="center",
                transform=trend_ax.transAxes
            )

        trend_figure.tight_layout()

        trend_canvas = FigureCanvasTkAgg(
            trend_figure,
            master=chart_frame
        )

        trend_canvas.draw()

        trend_canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )
        
        
        # ----------------------------------
        # Bandwidth Trend Chart
        # ----------------------------------

        bandwidth_frame = tk.LabelFrame(
            trend_content,
            text="Bandwidth Trends",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=10
        )

        bandwidth_frame.pack(
            fill="both",
            expand=False,
            padx=20,
            pady=5
        )
        
        bandwidth_frame.configure(
            height=320
        )

        bandwidth_frame.pack_propagate(False)

        bandwidth_figure = Figure(
            figsize=(10, 3.2),
            dpi=100
        )

        bandwidth_ax = bandwidth_figure.add_subplot(
            111
        )

        bandwidth_plotted = False

        # ----------------------------------
        # Download Speed
        # ----------------------------------

        if any(
            value is not None
            for value in download_series
        ):

            bandwidth_ax.plot(
                test_numbers,
                download_series,
                marker="o",
                linewidth=2,
                label="Download Speed (Mbps)"
            )

            bandwidth_plotted = True

        # ----------------------------------
        # Upload Speed
        # ----------------------------------

        if any(
            value is not None
            for value in upload_series
        ):

            bandwidth_ax.plot(
                test_numbers,
                upload_series,
                marker="o",
                linewidth=2,
                label="Upload Speed (Mbps)"
            )

            bandwidth_plotted = True

        bandwidth_ax.set_title(
            "Download and Upload Speed Trend"
        )

        bandwidth_ax.set_xlabel(
            "Test Number"
        )

        bandwidth_ax.set_ylabel(
            "Speed (Mbps)"
        )

        bandwidth_ax.grid(
            True
        )

        if bandwidth_plotted:

            bandwidth_ax.legend()

        else:

            bandwidth_ax.text(
                0.5,
                0.5,
                "No historical bandwidth data available",
                horizontalalignment="center",
                verticalalignment="center",
                transform=bandwidth_ax.transAxes
            )

        bandwidth_figure.tight_layout()

        bandwidth_canvas = FigureCanvasTkAgg(
            bandwidth_figure,
            master=bandwidth_frame
        )

        bandwidth_canvas.draw()

        bandwidth_canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        # ----------------------------------
        # Health Score Information
        # ----------------------------------

        health_frame = tk.Frame(
            trend_content,
            padx=20,
            pady=8
        )

        health_frame.pack(
            fill="x"
        )

        health_values = [
            value
            for value in health_series
            if value is not None
        ]

        if health_values:

            health_text = (
                f"Health Score Trend  |  "
                f"Average: "
                f"{trend_data['health_score']['average']}  |  "
                f"Minimum: "
                f"{trend_data['health_score']['minimum']}  |  "
                f"Maximum: "
                f"{trend_data['health_score']['maximum']}"
            )

        else:

            health_text = (
                "Health Score Trend  |  "
                "No data available"
            )

        tk.Label(
            health_frame,
            text=health_text,
            font=("Arial", 10, "bold"),
            anchor="w"
        ).pack(
            fill="x"
        )

    # ======================================
    # Open TXT Report
    # ======================================

    def open_text_report(self):

        filepath = os.path.abspath(
            os.path.join(
                "data",
                "reports",
                "network_report.txt"
            )
        )

        if not os.path.exists(filepath):

            messagebox.showwarning(
                "Report Not Found",
                "TXT report has not been generated yet.\n\n"
                "Run a network test first."
            )

            return

        try:

            os.startfile(
                filepath
            )

        except Exception as error:

            messagebox.showerror(
                "Unable to Open Report",
                f"Could not open TXT report:\n\n{error}"
            )

    # ======================================
    # Open CSV Report
    # ======================================

    def open_csv_report(self):

        filepath = os.path.abspath(
            os.path.join(
                "data",
                "reports",
                "network_report.csv"
            )
        )

        if not os.path.exists(filepath):

            messagebox.showwarning(
                "Report Not Found",
                "CSV report has not been generated yet.\n\n"
                "Run a network test first."
            )

            return

        try:

            os.startfile(
                filepath
            )

        except Exception as error:

            messagebox.showerror(
                "Unable to Open Report",
                f"Could not open CSV report:\n\n{error}"
            )

    # ======================================
    # Error Handler
    # ======================================

    def show_error(self, error):

        self.test_button.config(
            state="normal",
            text="START NETWORK TEST"
        )

        self.status_var.set(
            "Test failed"
        )

        messagebox.showerror(
            "Network Test Error",
            f"An error occurred:\n\n{error}"
        )


# ==========================================
# Run Dashboard
# ==========================================

def run_dashboard():

    root = tk.Tk()

    NPATDashboard(
        root
    )

    root.mainloop()


if __name__ == "__main__":

    run_dashboard()