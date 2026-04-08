chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {

    if (changeInfo.status === "complete" && tab.url && tab.url.startsWith("http")) {

        fetch("https://phishing-ml-api-gl9k.onrender.com/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: tab.url })
        })
        .then(res => res.json())
        .then(data => {
            console.log("API Response:", data);  // 👈 IMPORTANT

            chrome.scripting.executeScript({
                target: { tabId: tabId },
                func: showBanner,
                args: [data]
            });
        })
        .catch(err => console.error("API Error:", err));
    }
});
function showBanner(data) {

    if (document.getElementById("security-banner")) return;

    const banner = document.createElement("div");
    banner.id = "security-banner";

    const isPhishing = data.result.includes("Phishing");

    banner.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;">

            <div>
                ${isPhishing ? "⚠ Phishing Detected" : "✔ Safe Website"} <br>
                Confidence: ${data.confidence}% | Risk: ${data.risk_level}
            </div>

            <div>
                ${isPhishing ? `
                    <button id="backBtn">Go Back</button>
                    <button id="proceedBtn">Proceed</button>
                ` : ""}

                <button id="closeBtn">✖</button>
            </div>

        </div>
    `;

    banner.style.position = "fixed";
    banner.style.top = "0";
    banner.style.width = "100%";
    banner.style.padding = "12px";
    banner.style.color = "white";
    banner.style.zIndex = "999999";

    banner.style.background = isPhishing
        ? "linear-gradient(red, darkred)"
        : "linear-gradient(green, darkgreen)";

    document.body.prepend(banner);

    document.getElementById("closeBtn").onclick = () => banner.remove();

    if (isPhishing) {
        document.getElementById("backBtn").onclick = () => window.history.back();
        document.getElementById("proceedBtn").onclick = () => banner.remove();
    }
}