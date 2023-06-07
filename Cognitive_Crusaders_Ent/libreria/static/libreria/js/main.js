const getOptionChart = async (label, fechaInicio, fechaFin) => {
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/libreria/get_chart?label=${label}&fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`
    );
    return await response.json();
  } catch (ex) {
    alert(ex);
  }
};

const iniChart = async () => {
  const selectLabel = document.getElementById("select-label");
  const fechaInicioInput = document.getElementById("fecha-inicio");
  const fechaFinInput = document.getElementById("fecha-fin");
  const myChart = echarts.init(document.getElementById("chart"));

  const updateBtn = document.getElementById("update-btn");
  updateBtn.addEventListener("click", async () => {
    const label = selectLabel.value;
    const fechaInicio = fechaInicioInput.value;
    const fechaFin = fechaFinInput.value;
    myChart.clear();
    myChart.setOption(await getOptionChart(label, fechaInicio, fechaFin));
    myChart.resize();
  });
};

window.addEventListener("load", async()=>{
  await iniChart();
});