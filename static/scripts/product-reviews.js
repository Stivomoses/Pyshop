const totalReviews = JSON.parse(document.querySelector('#totalreviews').textContent);
const fivestars = JSON.parse(document.querySelector('#fivestars').textContent);
const fourstars = JSON.parse(document.querySelector('#fourstars').textContent);
const threestars = JSON.parse(document.querySelector('#threestars').textContent);
const twostars = JSON.parse(document.querySelector('#twostars').textContent);
const onestars = JSON.parse(document.querySelector('#onestars').textContent);

function percentageWidth(value, stars) {
  const percentage = (value / totalReviews) * 100;
  document.querySelector(`.js-graph-${stars}`).style.width = `${percentage}%`;
}

percentageWidth(fivestars, 5);
percentageWidth(fourstars, 4);
percentageWidth(threestars, 3);
percentageWidth(twostars, 2);
percentageWidth(onestars, 1);