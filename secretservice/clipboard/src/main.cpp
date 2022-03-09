#include <QGuiApplication>
#include <QClipboard>
#include <QMimeData>
#include <QByteArray>
#include <QTimer>

#include <iostream>

void copyToClipboard(const QByteArray &content, bool passwordManagerHint = false)
{
    const auto clipboard = QGuiApplication::clipboard();
    if (!clipboard)
    {
        return;
    }

    auto *mime = new QMimeData();

    const QString text = QString::fromUtf8(content);

    // copy with password manager hint enabled, clipboard manager may ignore or hide this entry
    if (passwordManagerHint)
    {
        mime->setText(text);
        mime->setData("x-kde-passwordManagerHint", QByteArrayLiteral("secret"));
        clipboard->setMimeData(mime, QClipboard::Clipboard);

        if (clipboard->supportsSelection())
        {
            clipboard->setMimeData(mime, QClipboard::Selection);
        }
    }

    // copy as plaintext, revealing the content to clipboard managers
    else
    {
        clipboard->setText(text);
    }
}

int main_daemon(QGuiApplication &a)
{
    // TODO:
    return 5;
}

int main(int argc, char **argv)
{
    QGuiApplication a(argc, argv);

    // run in daemon mode
    // if (argc > 1 && std::strcmp(argv[1], "--daemon") == 0)
    // {
    //     return main_daemon(a);
    // }

    // perform singleshot execution and quit
    QTimer shutdownTimer;

    QByteArray content;

    // read from stdin until EOF
    while (!std::cin.eof())
    {
        char arr[1024];
        std::cin.read(arr, sizeof(arr));
        int s = std::cin.gcount();
        content.append(arr, s);
    }

    // copy received content to clipboard if it isn't empty
    if (content.size() > 0)
    {
        // need to copy without password manager hint, so clipboard content isn't lost on program termination
        copyToClipboard(content, false);
    }

    // forcefully process Qt events
    a.processEvents();

    // give the clipboard manager enough time to mirror the data
    shutdownTimer.singleShot(100, [&]{
        // hopefully the clipboard manager did its work, now terminate because this is not a daemon
        a.exit();
    });

    return a.exec();
}
