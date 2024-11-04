// 配列をシャッフルする関数
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

// ウィジェットデータをCSVから読み込む関数
function loadWidgetsFromCSV(widgetId, start, end) {
  fetch('https://momi-100.com/blogparts/2024-11-04/data.csv') // CSVファイルのURLを指定
    .then(response => {
      if (!response.ok) {
        throw new Error("HTTP error, status = " + response.status);
      }
      return response.text();
    })
    .then(csvData => {
      // CSVデータを行ごとに分割し、各行をカンマで分割して配列にする
      const rows = csvData.split('\n').map(row => row.split(','));

      // 必要な範囲のデータを取得してランダムにシャッフル
      const widgetItems = [];
      for (let i = start; i < end; i++) {
        if (rows[i]) {
          const [title, link, img] = rows[i];
          widgetItems.push({ img, title, link });
        }
      }

      // スマホの場合は表示数を4つに制限
      if (window.innerWidth <= 768) {
        widgetItems.length = 4; // スマホ時は4つに制限
      }

      // アイテムをシャッフル
      shuffleArray(widgetItems);

      // ウィジェットアイテムを表示
      displayWidgetItems(widgetId, widgetItems);
    })
    .catch(error => console.error("データ取得エラー:", error));
}

// ウィジェットアイテムを表示する関数
function displayWidgetItems(widgetId, items) {
  const html = items.map(item => {
    // タイトルが26文字を超えた場合、末尾に「...」を追加
    const truncatedTitle = item.title.length > 26 ? item.title.substring(0, 26) + '...' : item.title;
    return `
      <a href="${item.link}">
        <img src="${item.img}" alt="${item.title}">
        <div class="title">${truncatedTitle}</div>
      </a>
    `;
  }).join('');

  document.getElementById(widgetId).innerHTML = html;
}

// 各ウィジェットにデータをロード
loadWidgetsFromCSV('blog-widget-1', 0, 6);   // 最初の6つのアイテム
loadWidgetsFromCSV('blog-widget-2', 6, 12);  // 次の6つのアイテム
loadWidgetsFromCSV('blog-widget-3', 12, 18); // さらに6つのアイテム
