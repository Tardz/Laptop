#include <gtkmm.h>
#include <giomm.h>
#include <gdkmm.h>
#include <iostream>
#include <pulse/pulseaudio.h>

class VolumeMenu : public Gtk::Window {
public:
    VolumeMenu(std::string pid_file_path);
    ~VolumeMenu();

private:
    void initializeResources();
    void setupUI();
    void createTitle();
    void createList();
    void volumeClicked();
    void soundOutputClicked(GdkEventButton* buttonEvent, const std::string& sinkName);
    std::string getActiveSink();
    bool getSoundOn();
    void updateListWithSoundOutputs();
    void addTestOutputs(int n);
    void getMousePosition(int& x, int& y);
    void onFocusOut(GdkEventFocus* event);
    void onEscapePress(GdkEventKey* event);
    void handleSigterm(int signum);
    void exitRemovePid();

    Gtk::Box mainBox;
    Gtk::Label title, desc, icon;
    Gtk::ScrolledWindow scrolledWindow;
    Gtk::ListBox list;
    pa_mainloop* paMainLoop;
    pa_context* paContext;
    bool soundOn;
    bool ignoreFocusLost;
    std::string pidFilePath;
};

VolumeMenu::VolumeMenu(std::string pid_file_path)
    : mainBox(Gtk::ORIENTATION_VERTICAL, 8),
      scrolledWindow(),
      list(),
      paMainLoop(nullptr),
      paContext(nullptr),
      soundOn(false),
      ignoreFocusLost(false),
      pidFilePath(pid_file_path) {

    initializeResources();
    setupUI();
    GLib::signal_idle().connect(sigc::mem_fun(*this, &VolumeMenu::updateListWithSoundOutputs));
}

VolumeMenu::~VolumeMenu() {
    pa_context_disconnect(paContext);
    pa_mainloop_free(paMainLoop);
}

void VolumeMenu::initializeResources() {
    signal(SIGTERM, &VolumeMenu::handleSigterm);
    signal(SIGINT, &VolumeMenu::handleSigterm);

    paMainLoop = pa_mainloop_new();
    paMainLoopAPI = pa_mainloop_get_api(paMainLoop);
    paContext = pa_context_new(paMainLoopAPI, "VolumeMenu");

    pa_context_connect(paContext, nullptr, PA_CONTEXT_NOFLAGS, nullptr);
    pa_mainloop_run(paMainLoop, nullptr);
}

void VolumeMenu::setupUI() {
    int x, y;
    getMousePosition(x, y);
    set_position(Gtk::WIN_POS_CENTER);
    set_size_request(290, 220);
    set_name("root");

    add(mainBox);

    createTitle();
    createList();

    mainBox.grab_focus();
    show_all();
}

void VolumeMenu::createTitle() {
    Gtk::Box titleBox(Gtk::ORIENTATION_HORIZONTAL, 0);
    titleBox.get_style_context()->add_class("toggle-box");

    Gtk::Box descBox(Gtk::ORIENTATION_VERTICAL, 0);

    title.set_halign(Gtk::ALIGN_START);
    title.get_style_context()->add_class("toggle-title");
    title.set_text("Outputs");

    desc.set_halign(Gtk::ALIGN_START);
    desc.get_style_context()->add_class("toggle-desc");
    if (!soundOn) {
        desc.set_text("Off");
    }

    Gtk::EventBox leftBox;
    Gtk::Box iconBox(Gtk::ORIENTATION_HORIZONTAL, 0);

    icon.set_halign(Gtk::ALIGN_START);
    icon.get_style_context()->add_class("toggle-icon");
    icon.set_text("");

    if (soundOn) {
        icon.set_name("toggle-icon-enabled");
    } else {
        icon.set_name("toggle-icon-disabled");
    }

    iconBox.pack_start(icon, false, false, 0);
    leftBox.add(iconBox);
    descBox.pack_start(title, false, false, 0);
    descBox.pack_start(desc, false, false, 0);
    titleBox.pack_start(leftBox, false, false, 0);
    titleBox.pack_start(descBox, false, false, 0);

    leftBox.signal_button_press_event().connect(sigc::mem_fun(*this, &VolumeMenu::volumeClicked));
    mainBox.pack_start(titleBox, false, false, 0);
}

void VolumeMenu::createList() {
    mainBox.pack_start(scrolledWindow, true, true, 0);
    scrolledWindow.add(list);
    list.set_selection_mode(Gtk::SELECTION_NONE);

    // Uncomment the line below to add test outputs
    // addTestOutputs(2);
}

void VolumeMenu::volumeClicked() {
    if (soundOn) {
        soundOn = false;
        desc.set_text("Muted");
        icon.set_text("");
        // Other logic for muting
        icon.set_name("toggle-icon-disabled");
    } else {
        soundOn = true;
        icon.set_text("");
        // Other logic for unmuting
        icon.set_name("toggle-icon-enabled");
        updateListWithSoundOutputs();
    }
}

void VolumeMenu::soundOutputClicked(GdkEventButton* buttonEvent, pulsectl::Sink sink) {
    // Logic when a sound output is clicked
}

pulsectl::Sink VolumeMenu::getActiveSink() {
    // Logic to get the active sink
    return pulsectl::Sink();
}

bool VolumeMenu::getSoundOn() {
    return soundOn;
}

void VolumeMenu::updateListWithSoundOutputs() {
    // Logic to update the list with sound outputs
    return false;
}

void VolumeMenu::addTestOutputs(int n) {
    // Logic to add test outputs
}

void VolumeMenu::getMousePosition(int& x, int& y) {
    // Logic to get the mouse position
}

void VolumeMenu::onFocusOut(GdkEventFocus* event) {
    if (!ignoreFocusLost) {
        exitRemovePid();
    }
}

void VolumeMenu::onEscapePress(GdkEventKey* event) {
    if (event->keyval == GDK_KEY_Escape) {
        exitRemovePid();
    }
}

void VolumeMenu::handleSigterm(int signum) {
    exitRemovePid();
}

void VolumeMenu::exitRemovePid() {
    // Logic to handle SIGTERM or Escape press and remove pid file
    std::cout << "Exiting..." << std::endl;
    std::exit(0);
}

int main(int argc, char* argv[]) {
    auto app = Gtk::Application::create(argc, argv, "org.example.volume_menu");

    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <pid_file_path>" << std::endl;
        return 1;
    }

    std::string pid_file_path(argv[1]);
    VolumeMenu volumeMenu(pid_file_path);

    return app->run(volumeMenu);
}