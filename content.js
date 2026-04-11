window.addEventListener("message", (event) => {
    if (event.data.type === "SHOW_BANNER") {
        showBanner(event.data.payload);
    }
});

function showBanner(data) {

    console.log("Banner received:", data);

    if (document.getElementById("security-banner")) return;

    const banner = document.createElement("div");
    banner.id = "security-banner";

    const isPhishing = data.result.includes("Phishing");

    banner.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;font-family:sans-serif;">
            <div>
                ${isPhishing ? "⚠ Phishing Website Detected" : "✔ Safe Website"}<br>
                Confidence: ${data.confidence}% | Risk: ${data.risk_level}
            </div>
            <div>
                <button id="closeBtn">✖</button>
            </div>
        </div>
    `;

    banner.style.position = "fixed";
    banner.style.top = "0";
    banner.style.left = "0";
    banner.style.width = "100%";
    banner.style.padding = "12px";
    banner.style.color = "white";
    banner.style.zIndex = "999999";

    banner.style.background = isPhishing
        ? "linear-gradient(red, darkred)"
        : "linear-gradient(green, darkgreen)";

    document.body.prepend(banner);

    document.getElementById("closeBtn").onclick = () => banner.remove();
}