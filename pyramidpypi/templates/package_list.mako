<!DOCTYPE html>
<html>
<head>
    <title>${title}</title>
</head>
<body>
    % for link, package in zip(links, packages):
        <a href="${link}">${package}</a><br/>
    % endfor
</body>
</html>
