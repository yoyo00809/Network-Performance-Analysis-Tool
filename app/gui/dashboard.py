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

from app.database.database import (
    create_database,
    get_test_history,
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
            "1200x900"
        )

        self.root.minsize(
            1100,
            800
        )

        # ----------------------------------
        # Variables
        # ----------------------------------

        self.host_var = tk.StringVar()

        self.status_var = tk.StringVar(
            value="Ready"
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
            self.root,
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
            self.root,
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
    # Metrics Section
    # ======================================

    def create_metrics_section(self):

        section = tk.Frame(
            self.root,
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
            self.root,
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

    # ======================================
    # Performance Chart
    # ======================================

    def create_chart_section(self):

        section = tk.LabelFrame(
            self.root,
            text="Ping Response Time",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=5
        )

        section.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=8
        )

        self.figure = Figure(
            figsize=(8, 3),
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
            self.root,
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
            self.root,
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
            self.root,
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
                count=4
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

        report = generate_text_report(
            result["host"],
            ping_result,
            metrics,
            analysis,
            recommendations
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
            analysis
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

            health_score = record["health_score"]

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

            os.startfile(filepath)

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

            os.startfile(filepath)

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

    NPATDashboard(root)

    root.mainloop()


if __name__ == "__main__":
    run_dashboard()