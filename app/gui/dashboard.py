# ==========================================
# Network Performance Analysis Tool (NPAT)
# GUI Dashboard
# ==========================================

import tkinter as tk
from tkinter import messagebox
import threading

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from app.monitoring.monitor import monitor_once


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
            "1000x850"
        )

        self.root.minsize(
            900,
            750
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

        # ----------------------------------
        # Build Interface
        # ----------------------------------

        self.create_header()
        self.create_input_section()
        self.create_metrics_section()
        self.create_chart_section()
        self.create_analysis_section()
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

        # Create Matplotlib figure

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
                "Packet Loss    : --"
            ),
            font=("Arial", 11),
            justify="left",
            anchor="w"
        )

        self.analysis_text.pack(
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
            pady=(5, 15)
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

        recommendations = result["recommendations"]

        ping_result = result["ping"]

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
                f"{analysis['packet_loss_status']}"
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