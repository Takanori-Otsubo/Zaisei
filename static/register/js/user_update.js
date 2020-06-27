const departmentElement = $('#id_department');
const sectionElement = $('#id_section');

const changeSection = (select) => {
    // 子カテゴリの選択欄を空にする。
    sectionElement.children().remove();

    // 選択した親カテゴリに紐づく子カテゴリの一覧を取得する。
    const departmentId = departmentElement.val();
    const sectionList = section[departmentId];
    
    // 子カテゴリの選択肢を作成・追加。
    for (const section of sectionList) {
        const option = $('<option>');
        option.val(section['pk']);
        option.text(section['name']);
        sectionElement.append(option);
    }

    // 指定があれば、そのカテゴリを選択する
    if (select !== undefined) {
        sectionElement.val(select);
    }
};

departmentElement.on('change', () => {
    changeSection();
});

// 入力値に問題があって再表示された場合、ページ表示時点で小カテゴリが絞り込まれるようにする
if (departmentElement.val()) {
    const selectedSection = sectionElement.val();
    changeSection(selectedSection);
}