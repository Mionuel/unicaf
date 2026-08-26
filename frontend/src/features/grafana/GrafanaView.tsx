const GrafanaViewer = () => {
  const grafanaUrl =
    "http://localhost:3000/d/adl9cr4/my-dashboard?orgId=1&from=now-6h&to=now&timezone=browser";

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <iframe
        src={grafanaUrl}
        width="100%"
        height="100%"
        title="Grafana Dashboard"
        style={{ flexGrow: 1, border: "none" }}
      />
    </div>
  );
};

export default GrafanaViewer;
