#include <QGuiApplication>
#include <QClipboard>
#include <QMimeData>
#include <QByteArray>
#include <QTimer>

#include <iostream>

void copyToClipboard(const QByteArray &content)
{
    const auto clipboard = QGuiApplication::clipboard();
    if (!clipboard)
    {
        return;
    }

    auto *mime = new QMimeData();

    const QString text = QString::fromUtf8(content);

//     mime->setText(text);
//     mime->setData("x-kde-passwordManagerHint", QByteArrayLiteral("secret"));
//     clipboard->setMimeData(mime, QClipboard::Clipboard);
// 
//     if (clipboard->supportsSelection())
//     {
//         clipboard->setMimeData(mime, QClipboard::Selection);
//     }

    clipboard->setText(text);
}

int main(int argc, char **argv)
{
    QGuiApplication a(argc, argv);
    QTimer shutdownTimer;

    QByteArray content;

    while (!std::cin.eof())
    {
        char arr[1024];
        std::cin.read(arr, sizeof(arr));
        int s = std::cin.gcount();
        content.append(arr, s);
    }

    if (content.size() > 0)
    {
        copyToClipboard(content);
    }

    a.processEvents();

    // give the clipboard manager enough time to mirror the data
    shutdownTimer.singleShot(100, [&]{
        // hopefully the clipboard manager did its work, now terminate because this is not a daemon
        a.exit();
    });

    return a.exec();
}
