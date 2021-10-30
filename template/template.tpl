<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>目標設定</title>
</head>

<body>
    <h1><span>{{ Do_num }}</span>{{ Title }}</h1>

    {% for content in Contents %}
    <div class="content">
        <div class="content-item">{{ content.content_title }}</div>
        <p>{{ content.content_value }}</p>
    </div>
    {% endfor %}

</body>
</html>
