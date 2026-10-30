import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';
import 'package:shared_preferences/shared_preferences.dart';

// ==========================================================
// PYTHONANYWHERE PERMANENT SERVER & TELEGRAM CONFIGURATION
// ==========================================================
const String serverUrl = 'https://Alibaba786.pythonanywhere.com';
const String telegramBotToken = '8484105200:AAE4z7_EOf_RwE9xUAu7EPSChNXiy4PMcZE';
const String telegramChatId = '8052842442';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const PK786App());
}

class PK786App extends StatelessWidget {
  const PK786App({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PK786 Casino',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0A0A0E),
        primaryColor: const Color(0xFFFFD700),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFFFFD700),
          secondary: Color(0xFFFF2A6D),
          surface: Color(0xFF161622),
        ),
      ),
      home: const SplashScreen(),
    );
  }
}

// ==========================================================
// UNIVERSAL BACKGROUND SCAFFOLD HELPER
// ==========================================================
Widget buildThemedScaffold({
  required String title,
  required Widget body,
  List<Widget>? actions,
  Widget? bottomNavigationBar,
}) {
  return Scaffold(
    appBar: AppBar(
      title: Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
      backgroundColor: const Color(0xFF101018).withOpacity(0.9),
      actions: actions,
    ),
    body: Stack(
      children: [
        Positioned.fill(
          child: Image.network(
            'https://raw.githubusercontent.com/827vzizb/Bsksnwbs/refs/heads/raw/IMG-20261030-WA2592.jpg',
            fit: BoxFit.cover,
          ),
        ),
        Positioned.fill(
          child: Container(
            color: Colors.black.withOpacity(0.82),
          ),
        ),
        body,
      ],
    ),
    bottomNavigationBar: bottomNavigationBar,
  );
}

// ==========================================================
// PUBG STYLE TOP OVERLAY NOTIFICATION HELPER (3 SECONDS)
// ==========================================================
void showPubgBanner(BuildContext context, String message, {bool isWin = false}) {
  OverlayEntry? overlayEntry;
  overlayEntry = OverlayEntry(
    builder: (context) => Positioned(
      top: MediaQuery.of(context).padding.top + 10,
      left: 20,
      right: 20,
      child: Material(
        color: Colors.transparent,
        child: TweenAnimationBuilder<double>(
          tween: Tween(begin: 0.0, end: 1.0),
          duration: const Duration(milliseconds: 300),
          builder: (context, value, child) {
            return Transform.scale(
              scale: value,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                decoration: BoxDecoration(
                  color: isWin ? Colors.green.shade800 : Colors.black87,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: isWin ? Colors.greenAccent : const Color(0xFFFFD700), width: 2),
                  boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 10, offset: Offset(0, 4))],
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(isWin ? Icons.celebration : Icons.notifications_active, color: const Color(0xFFFFD700)),
                    const SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        message,
                        style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    ),
  );

  Overlay.of(context).insert(overlayEntry);
  Future.delayed(const Duration(seconds: 3), () {
    overlayEntry?.remove();
  });
}

// ==========================================================
// SAFE SPLASH SCREEN
// ==========================================================
class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    _checkSession();
  }

  void _checkSession() async {
    try {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      bool isLoggedIn = prefs.getBool('isLoggedIn') ?? false;
      String username = prefs.getString('username') ?? '';
      String phone = prefs.getString('phone') ?? '';

      if (!mounted) return;
      if (isLoggedIn && username.isNotEmpty) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => MainDashboard(username: username, phone: phone)),
        );
      } else {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => const LoginScreen()),
        );
      }
    } catch (e) {
      if (!mounted) return;
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const LoginScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF0A0A0E), Color(0xFF1F1A3A)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.casino, size: 90, color: Color(0xFFFFD700)),
              SizedBox(height: 16),
              Text(
                'PK786 CASINO',
                style: TextStyle(fontSize: 28, fontWeight: FontWeight.w900, color: Color(0xFFFFD700), letterSpacing: 3),
              ),
              SizedBox(height: 30),
              CircularProgressIndicator(color: Color(0xFFFFD700)),
            ],
          ),
        ),
      ),
    );
  }
}

// ==========================================================
// 1. LOGIN & OLD ID RECOVERY SCREEN
// ==========================================================
class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _usernameController = TextEditingController();
  final _phoneController = TextEditingController();
  final _paymentController = TextEditingController();
  bool isLoggingIn = false;

  void _handleRegisterOrLogin({bool isOldLogin = false}) async {
    String username = _usernameController.text.trim().replaceAll('@', '');
    String phone = _phoneController.text.trim();

    if (username.isEmpty) {
      showPubgBanner(context, 'Username is required!');
      return;
    }

    if (!isOldLogin && phone.isEmpty) {
      showPubgBanner(context, 'Phone Number is required for new registration!');
      return;
    }

    if (!isOldLogin && _paymentController.text.trim().isEmpty) {
      showPubgBanner(context, 'Payment Account ID is required!');
      return;
    }

    setState(() => isLoggingIn = true);

    try {
      final endpoint = isOldLogin ? '$serverUrl/api/login' : '$serverUrl/api/register';
      final response = await http.post(
        Uri.parse(endpoint),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'username': username,
          'phone': phone,
          'bkash': _paymentController.text.trim(),
          'nagad': '',
        }),
      );

      setState(() => isLoggingIn = false);

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['status'] == 'success') {
          SharedPreferences prefs = await SharedPreferences.getInstance();
          await prefs.setBool('isLoggedIn', true);
          await prefs.setString('username', username);
          await prefs.setString('phone', phone);

          if (!mounted) return;
          showPubgBanner(context, 'Welcome back, @$username!', isWin: true);
          Navigator.pushReplacement(
            context,
            MaterialPageRoute(builder: (context) => MainDashboard(username: username, phone: phone)),
          );
        } else {
          showPubgBanner(context, data['message'] ?? 'User not found! Check username and phone.');
        }
      } else {
        showPubgBanner(context, 'Server connection failed.');
      }
    } catch (e) {
      setState(() => isLoggingIn = false);
      showPubgBanner(context, 'Error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF0A0A0E), Color(0xFF1F1A3A)],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
        ),
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.casino, size: 80, color: Color(0xFFFFD700)),
                const SizedBox(height: 12),
                const Text(
                  'PK786',
                  style: TextStyle(fontSize: 38, fontWeight: FontWeight.w900, color: Color(0xFFFFD700), letterSpacing: 4),
                ),
                const Text('REAL CASINO EXPERIENCE', style: TextStyle(color: Colors.grey, fontSize: 12, letterSpacing: 2)),
                const SizedBox(height: 35),
                TextField(
                  controller: _usernameController,
                  decoration: InputDecoration(
                    labelText: 'Unique Username',
                    prefixIcon: const Icon(Icons.person, color: Color(0xFFFFD700)),
                    filled: true,
                    fillColor: const Color(0xFF161622),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: _phoneController,
                  keyboardType: TextInputType.phone,
                  decoration: InputDecoration(
                    labelText: 'Phone Number',
                    prefixIcon: const Icon(Icons.phone, color: Color(0xFFFFD700)),
                    filled: true,
                    fillColor: const Color(0xFF161622),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: _paymentController,
                  keyboardType: TextInputType.phone,
                  decoration: InputDecoration(
                    labelText: 'Payment Account ID (JazzCash/EasyPaisa/UPaisa)',
                    prefixIcon: const Icon(Icons.account_balance_wallet, color: Colors.amberAccent),
                    filled: true,
                    fillColor: const Color(0xFF161622),
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                ),
                const SizedBox(height: 30),
                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFFFFD700),
                      foregroundColor: Colors.black,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                    onPressed: isLoggingIn ? null : () => _handleRegisterOrLogin(isOldLogin: false),
                    child: isLoggingIn
                        ? const CircularProgressIndicator(color: Colors.black)
                        : const Text('CREATE NEW ACCOUNT', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  ),
                ),
                const SizedBox(height: 12),
                TextButton(
                  onPressed: isLoggingIn ? null : () => _handleRegisterOrLogin(isOldLogin: true),
                  child: const Text('Already have an ID? Login & Recover Coins', style: TextStyle(color: Color(0xFFFFD700), fontWeight: FontWeight.bold)),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

// ==========================================================
// 2. MAIN DASHBOARD WITH SERVER POLLING
// ==========================================================
class MainDashboard extends StatefulWidget {
  final String username;
  final String phone;

  const MainDashboard({super.key, required this.username, required this.phone});

  @override
  State<MainDashboard> createState() => _MainDashboardState();
}

class _MainDashboardState extends State<MainDashboard> {
  int _currentIndex = 0;
  double userCoins = 0.0;
  Timer? _serverPollTimer;

  @override
  void initState() {
    super.initState();
    _fetchServerBalance();
    _startServerSync();
  }

  void _fetchServerBalance() async {
    try {
      final response = await http.get(Uri.parse('$serverUrl/api/balance/${widget.username}'));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (mounted) {
          setState(() {
            userCoins = double.parse(data['coins'].toString());
          });
        }
      }
    } catch (e) {}
  }

  void _updateCoinsOnServer(double netChange) async {
    try {
      final response = await http.post(
        Uri.parse('$serverUrl/api/admin/add_coins'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'username': widget.username, 'amount': netChange}),
      );
      if (response.statusCode == 200) {
        _fetchServerBalance();
      }
    } catch (e) {}
  }

  void _startServerSync() {
    _serverPollTimer = Timer.periodic(const Duration(seconds: 4), (timer) {
      _fetchServerBalance();
    });
  }

  @override
  void dispose() {
    _serverPollTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final List<Widget> pages = [
      GamesHomeTab(username: widget.username, coins: userCoins, onUpdate: _updateCoinsOnServer),
      BuyCoinsTab(username: widget.username, phone: widget.phone),
      WithdrawTab(username: widget.username, coins: userCoins, onUpdate: _updateCoinsOnServer),
      MessageOwnerTab(username: widget.username, phone: widget.phone),
      ProfileTab(username: widget.username, phone: widget.phone, coins: userCoins),
    ];

    return Scaffold(
      body: pages[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        selectedItemColor: const Color(0xFFFFD700),
        unselectedItemColor: Colors.grey,
        backgroundColor: const Color(0xFF101018),
        type: BottomNavigationBarType.fixed,
        onTap: (index) => setState(() => _currentIndex = index),
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.sports_esports), label: 'Games'),
          BottomNavigationBarItem(icon: Icon(Icons.add_shopping_cart), label: 'Buy Coins'),
          BottomNavigationBarItem(icon: Icon(Icons.account_balance_wallet), label: 'Withdraw'),
          BottomNavigationBarItem(icon: Icon(Icons.support_agent), label: 'Support'),
          BottomNavigationBarItem(icon: Icon(Icons.account_circle), label: 'Account'),
        ],
      ),
    );
  }
}

// ==========================================================
// TAB 1: GAMES HOME TAB
// ==========================================================
class GamesHomeTab extends StatelessWidget {
  final String username;
  final double coins;
  final Function(double) onUpdate;

  const GamesHomeTab({super.key, required this.username, required this.coins, required this.onUpdate});

  @override
  Widget build(BuildContext context) {
    final games = [
      {
        'name': 'Aviator',
        'icon': Icons.flight_takeoff,
        'gradient': [Colors.redAccent, Colors.deepOrange],
        'widget': AviatorGame(username: username, coins: coins, onUpdate: onUpdate)
      },
      {
        'name': 'Casino Slots',
        'icon': Icons.casino,
        'gradient': [Colors.amber, Colors.orangeAccent],
        'widget': SlotsGame(username: username, coins: coins, onUpdate: onUpdate)
      },
      {
        'name': 'Lucky Spin Wheel',
        'icon': Icons.color_lens,
        'gradient': [Colors.purpleAccent, Colors.deepPurple],
        'widget': SpinGame(username: username, coins: coins, onUpdate: onUpdate)
      },
      {
        'name': 'High Low Dice',
        'icon': Icons.style,
        'gradient': [Colors.blueAccent, Colors.indigoAccent],
        'widget': DiceGame(username: username, coins: coins, onUpdate: onUpdate)
      },
      {
        'name': 'Minesweeper',
        'icon': Icons.grid_on,
        'gradient': [Colors.greenAccent, Colors.teal],
        'widget': MinesGame(username: username, coins: coins, onUpdate: onUpdate)
      },
      {
        'name': 'Limbo Rocket',
        'icon': Icons.rocket_launch,
        'gradient': [Colors.orangeAccent, Colors.red],
        'widget': LimboGame(username: username, coins: coins, onUpdate: onUpdate)
      },
    ];

    return buildThemedScaffold(
      title: 'PK786 CASINO - @$username',
      actions: [
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
          margin: const EdgeInsets.only(right: 16),
          decoration: BoxDecoration(
            color: const Color(0xFF1A1A2A),
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: const Color(0xFFFFD700)),
          ),
          child: Row(
            children: [
              const Icon(Icons.monetization_on, color: Color(0xFFFFD700), size: 18),
              const SizedBox(width: 6),
              Text('${coins.toStringAsFixed(0)} Coins', style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
            ],
          ),
        )
      ],
      body: Padding(
        padding: const EdgeInsets.all(12.0),
        child: GridView.builder(
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            crossAxisSpacing: 12,
            mainAxisSpacing: 12,
            childAspectRatio: 0.85,
          ),
          itemCount: games.length,
          itemBuilder: (context, index) {
            final game = games[index];
            final List<Color> colors = game['gradient'] as List<Color>;
            return GestureDetector(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => game['widget'] as Widget),
                );
              },
              child: Container(
                decoration: BoxDecoration(
                  color: const Color(0xFF161622),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: colors[0].withOpacity(0.6)),
                  boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.5), blurRadius: 8)],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Expanded(
                      flex: 6,
                      child: Container(
                        decoration: BoxDecoration(
                          borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
                          gradient: LinearGradient(colors: colors, begin: Alignment.topLeft, end: Alignment.bottomRight),
                        ),
                        child: Center(child: Icon(game['icon'] as IconData, size: 55, color: Colors.white)),
                      ),
                    ),
                    Expanded(
                      flex: 4,
                      child: Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(game['name'] as String, style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Colors.white), textAlign: TextAlign.center),
                            const SizedBox(height: 4),
                            Text('BET 100 - 30K', style: TextStyle(fontSize: 11, color: colors[0], fontWeight: FontWeight.bold)),
                          ],
                        ),
                      ),
                    )
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}

// ==========================================================
// TAB 2: BUY COINS (WITH UPDATED PAKISTANI ACCOUNTS & SCREENSHOT PROOF)
// ==========================================================
class BuyCoinsTab extends StatefulWidget {
  final String username;
  final String phone;

  const BuyCoinsTab({super.key, required this.username, required this.phone});

  @override
  State<BuyCoinsTab> createState() => _BuyCoinsTabState();
}

class _BuyCoinsTabState extends State<BuyCoinsTab> {
  final _trxController = TextEditingController();
  final _amountController = TextEditingController();
  String selectedMethod = 'JazzCash';
  File? _selectedImage;
  bool isUploading = false;

  Future<void> _pickImage() async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);
    if (pickedFile != null) {
      setState(() {
        _selectedImage = File(pickedFile.path);
      });
    }
  }

  void _submitDeposit() async {
    if (_trxController.text.isEmpty || _amountController.text.isEmpty) {
      showPubgBanner(context, 'Fill all fields!');
      return;
    }

    setState(() => isUploading = true);

    try {
      final response = await http.post(
        Uri.parse('$serverUrl/api/deposit'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'username': widget.username,
          'amount': _amountController.text,
          'method': selectedMethod,
          'trx': _trxController.text,
        }),
      );

      if (_selectedImage != null && telegramBotToken != 'YOUR_TELEGRAM_BOT_TOKEN_HERE') {
        var request = http.MultipartRequest(
          'POST',
          Uri.parse('https://api.telegram.org/bot$telegramBotToken/sendPhoto'),
        );
        request.fields['chat_id'] = telegramChatId;
        request.fields['caption'] = '💰 New Deposit Proof!\n👤 User: @${widget.username}\n💵 Amount: ${_amountController.text} PKR\n📱 Method: $selectedMethod\n🔖 TrxID: ${_trxController.text}';
        request.files.add(await http.MultipartFile.fromPath('photo', _selectedImage!.path));
        await request.send();
      }

      setState(() => isUploading = false);

      if (!mounted) return;

      if (response.statusCode == 200) {
        _trxController.clear();
        _amountController.clear();
        setState(() => _selectedImage = null);
        showPubgBanner(context, 'Deposit proof submitted successfully!', isWin: true);
      } else {
        showPubgBanner(context, 'Failed to submit deposit.');
      }
    } catch (e) {
      setState(() => isUploading = false);
      showPubgBanner(context, 'Error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return buildThemedScaffold(
      title: 'Buy Coins (1 PKR = 1 Coin)',
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFF161622),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: const Color(0xFFFFD700)),
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Official Accounts (Personal):', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFFFFD700))),
                  SizedBox(height: 8),
                  Text('• JazzCash: 03254135792\n  Name: Faizan Maqbool', style: TextStyle(fontSize: 14, color: Colors.white)),
                  SizedBox(height: 6),
                  Text('• UPaisa: 03054926639\n  Name: Parveen Kausar', style: TextStyle(fontSize: 14, color: Colors.white)),
                  SizedBox(height: 6),
                  Text('• Easypaisa: 03431044275\n  Name: Muhammad Awais', style: TextStyle(fontSize: 14, color: Colors.white)),
                  SizedBox(height: 10),
                  Text('⚠️ Payment Screenshot Proof Send Necessary!', style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.bold, fontSize: 13)),
                ],
              ),
            ),
            const SizedBox(height: 20),
            Row(
              children: [
                Expanded(
                  child: ChoiceChip(
                    label: const Text('JazzCash'),
                    selected: selectedMethod == 'JazzCash',
                    selectedColor: Colors.orange,
                    onSelected: (val) => setState(() => selectedMethod = 'JazzCash'),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: ChoiceChip(
                    label: const Text('UPaisa'),
                    selected: selectedMethod == 'UPaisa',
                    selectedColor: Colors.amber,
                    onSelected: (val) => setState(() => selectedMethod = 'UPaisa'),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: ChoiceChip(
                    label: const Text('Easypaisa'),
                    selected: selectedMethod == 'Easypaisa',
                    selectedColor: Colors.green,
                    onSelected: (val) => setState(() => selectedMethod = 'Easypaisa'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _amountController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(labelText: 'Amount (PKR)', filled: true, fillColor: const Color(0xFF161622), border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _trxController,
              decoration: InputDecoration(labelText: 'TrxID / Transaction Reference', filled: true, fillColor: const Color(0xFF161622), border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF161622), foregroundColor: const Color(0xFFFFD700)),
                  onPressed: _pickImage,
                  icon: const Icon(Icons.image),
                  label: Text(_selectedImage == null ? 'Select Payment Screenshot' : 'Screenshot Attached ✅'),
                ),
              ],
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFFFFD700), foregroundColor: Colors.black),
                onPressed: isUploading ? null : _submitDeposit,
                child: Text(isUploading ? 'UPLOADING...' : 'SUBMIT DEPOSIT PROOF', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ==========================================================
// TAB 3: COINS TO MONEY WITHDRAWAL SESSION (STRICT BALANCE CHECK)
// ==========================================================
class WithdrawTab extends StatefulWidget {
  final String username;
  final double coins;
  final Function(double) onUpdate;

  const WithdrawTab({super.key, required this.username, required this.coins, required this.onUpdate});

  @override
  State<WithdrawTab> createState() => _WithdrawTabState();
}

class _WithdrawTabState extends State<WithdrawTab> {
  final _amountController = TextEditingController();
  final _accController = TextEditingController();
  String selectedMethod = 'JazzCash';
  bool isSubmitting = false;

  void _submitWithdrawal() async {
    String amtStr = _amountController.text.trim();
    String acc = _accController.text.trim();

    if (amtStr.isEmpty || acc.isEmpty) {
      showPubgBanner(context, 'Enter amount and account number!');
      return;
    }

    double reqCoins = double.tryParse(amtStr) ?? 0;
    if (reqCoins <= 0) {
      showPubgBanner(context, 'Invalid withdrawal amount!');
      return;
    }

    if (reqCoins > widget.coins) {
      showPubgBanner(context, 'You have not this much coins!');
      return;
    }

    setState(() => isSubmitting = true);

    try {
      final response = await http.post(
        Uri.parse('$serverUrl/api/withdraw'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'username': widget.username,
          'amount': reqCoins,
          'method': selectedMethod,
          'account': acc,
        }),
      );

      setState(() => isSubmitting = false);

      if (!mounted) return;

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['status'] == 'success') {
          widget.onUpdate(-reqCoins);
          _amountController.clear();
          _accController.clear();
          showPubgBanner(context, 'Your withdrawn amount will come in your account under few hours!', isWin: true);
        } else {
          showPubgBanner(context, data['message'] ?? 'Withdrawal failed.');
        }
      } else {
        showPubgBanner(context, 'Server error during withdrawal.');
      }
    } catch (e) {
      setState(() => isSubmitting = false);
      showPubgBanner(context, 'Error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return buildThemedScaffold(
      title: 'Coins to Money Withdrawal',
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Available Balance: ${widget.coins.toStringAsFixed(0)} Coins', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Color(0xFFFFD700))),
            const SizedBox(height: 20),
            Row(
              children: [
                Expanded(
                  child: ChoiceChip(
                    label: const Text('JazzCash'),
                    selected: selectedMethod == 'JazzCash',
                    selectedColor: Colors.orange,
                    onSelected: (val) => setState(() => selectedMethod = 'JazzCash'),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: ChoiceChip(
                    label: const Text('UPaisa'),
                    selected: selectedMethod == 'UPaisa',
                    selectedColor: Colors.amber,
                    onSelected: (val) => setState(() => selectedMethod = 'UPaisa'),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: ChoiceChip(
                    label: const Text('Easypaisa'),
                    selected: selectedMethod == 'Easypaisa',
                    selectedColor: Colors.green,
                    onSelected: (val) => setState(() => selectedMethod = 'Easypaisa'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _amountController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(labelText: 'Coins to Withdraw', filled: true, fillColor: const Color(0xFF161622), border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _accController,
              keyboardType: TextInputType.phone,
              decoration: InputDecoration(labelText: 'Account Number ($selectedMethod)', filled: true, fillColor: const Color(0xFF161622), border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFFFFD700), foregroundColor: Colors.black),
                onPressed: isSubmitting ? null : _submitWithdrawal,
                child: Text(isSubmitting ? 'PROCESSING...' : 'WITHDRAW COINS', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ==========================================================
// TAB 4: MESSAGE OWNER
// ==========================================================
class MessageOwnerTab extends StatefulWidget {
  final String username;
  final String phone;

  const MessageOwnerTab({super.key, required this.username, required this.phone});

  @override
  State<MessageOwnerTab> createState() => _MessageOwnerTabState();
}

class _MessageOwnerTabState extends State<MessageOwnerTab> {
  final _msgController = TextEditingController();
  bool isSending = false;

  void _sendMessageToOwner() async {
    String text = _msgController.text.trim();
    if (text.isEmpty) {
      showPubgBanner(context, 'Please write a message!');
      return;
    }

    setState(() => isSending = true);

    try {
      final response = await http.post(
        Uri.parse('$serverUrl/api/deposit'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'username': widget.username,
          'amount': '0',
          'method': 'Support Msg',
          'trx': text,
        }),
      );

      setState(() => isSending = false);

      if (!mounted) return;

      if (response.statusCode == 200) {
        _msgController.clear();
        showPubgBanner(context, 'Message sent successfully!', isWin: true);
      } else {
        showPubgBanner(context, 'Failed to send message.');
      }
    } catch (e) {
      setState(() => isSending = false);
      showPubgBanner(context, 'Error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return buildThemedScaffold(
      title: 'Support & Message Owner',
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('Have questions or support issues? Send a message directly to the owner.', style: TextStyle(color: Colors.grey, fontSize: 14)),
            const SizedBox(height: 20),
            TextField(
              controller: _msgController,
              maxLines: 5,
              decoration: InputDecoration(labelText: 'Type your message...', filled: true, fillColor: const Color(0xFF161622), border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFFFFD700), foregroundColor: Colors.black),
                onPressed: isSending ? null : _sendMessageToOwner,
                child: isSending ? const CircularProgressIndicator(color: Colors.black) : const Text('SEND MESSAGE', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ==========================================================
// TAB 5: ACCOUNT TAB WITH LOGOUT
// ==========================================================
class ProfileTab extends StatelessWidget {
  final String username;
  final String phone;
  final double coins;

  const ProfileTab({super.key, required this.username, required this.phone, required this.coins});

  void _logout(BuildContext context) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    if (!context.mounted) return;
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => const LoginScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return buildThemedScaffold(
      title: 'My PK786 Account',
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(
              child: Column(
                children: [
                  const CircleAvatar(radius: 40, backgroundColor: Color(0xFFFFD700), child: Icon(Icons.person, size: 40, color: Colors.black)),
                  const SizedBox(height: 10),
                  Text('@$username', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                  Text(phone, style: const TextStyle(color: Colors.grey)),
                ],
              ),
            ),
            const SizedBox(height: 30),
            Card(
              color: const Color(0xFF161622),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: ListTile(
                leading: const Icon(Icons.monetization_on, color: Color(0xFFFFD700)),
                title: const Text('Coins Balance'),
                trailing: Text('${coins.toStringAsFixed(0)} Coins', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFFFFD700))),
              ),
            ),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.redAccent, foregroundColor: Colors.white),
                onPressed: () => _logout(context),
                child: const Text('LOGOUT', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ==========================================================
// UNIVERSAL BET SELECTOR WIDGET
// ==========================================================
class BetSelectorWidget extends StatelessWidget {
  final double currentBet;
  final Function(double) onBetChanged;

  const BetSelectorWidget({super.key, required this.currentBet, required this.onBetChanged});

  @override
  Widget build(BuildContext context) {
    List<double> bets = [100, 500, 1000, 5000, 10000, 30000];
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text('Select Bet Amount:', style: TextStyle(color: Colors.grey, fontWeight: FontWeight.bold)),
            Text('${currentBet.toStringAsFixed(0)} Coins', style: const TextStyle(color: Color(0xFFFFD700), fontWeight: FontWeight.bold)),
          ],
        ),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8,
          children: bets.map((amt) {
            return ChoiceChip(
              label: Text('${amt.toStringAsFixed(0)}'),
              selected: currentBet == amt,
              selectedColor: const Color(0xFFFFD700),
              labelStyle: TextStyle(color: currentBet == amt ? Colors.black : Colors.white, fontWeight: FontWeight.bold),
              onSelected: (val) => onBetChanged(amt),
            );
          }).toList(),
        ),
      ],
    );
  }
}

// ==========================================================
// GAME 1: AVIATOR CRASH (PROFESSIONAL FULL SCREEN ANIMATION)
// ==========================================================
class AviatorGame extends StatefulWidget {
  final String username;
  final double coins;
  final Function(double) onUpdate;

  const AviatorGame({super.key, required this.username, required this.coins, required this.onUpdate});

  @override
  State<AviatorGame> createState() => _AviatorGameState();
}

class _AviatorGameState extends State<AviatorGame> with SingleTickerProviderStateMixin {
  double multiplier = 1.00;
  bool isPlaying = false;
  bool hasCrashed = false;
  Timer? _timer;
  double betAmount = 100;
  late AnimationController _animController;

  @override
  void initState() {
    super.initState();
    _animController = AnimationController(vsync: this, duration: const Duration(seconds: 2)) ..repeat(reverse: true);
  }

  @override
  void dispose() {
    _timer?.cancel();
    _animController.dispose();
    super.dispose();
  }

  void startGame() {
    if (widget.coins < betAmount) {
      showPubgBanner(context, 'Insufficient Coins!');
      return;
    }
    widget.onUpdate(-betAmount);
    setState(() {
      multiplier = 1.00;
      isPlaying = true;
      hasCrashed = false;
    });

    double crashPoint = Random().nextDouble() < 0.75 ? (1.0 + Random().nextDouble() * 0.3) : (1.3 + Random().nextDouble() * 1.5);

    _timer = Timer.periodic(const Duration(milliseconds: 100), (timer) {
      setState(() {
        multiplier += 0.05;
        if (multiplier >= crashPoint) {
          _timer?.cancel();
          isPlaying = false;
          hasCrashed = true;
          showPubgBanner(context, 'Crashed at ${multiplier.toStringAsFixed(2)}x! You Lost.');
        }
      });
    });
  }

  void cashOut() {
    if (!isPlaying) return;
    _timer?.cancel();
    double winAmount = betAmount * multiplier;
    setState(() => isPlaying = false);

    widget.onUpdate(winAmount);
    showPubgBanner(context, 'Congratulations You win ${winAmount.toStringAsFixed(0)} PKR Coins (1 Coins = 1 PKR)', isWin: true);
  }

  @override
  Widget build(BuildContext context) {
    return buildThemedScaffold(
      title: 'Aviator Flight',
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // Banner Image
            ClipRRect(
              borderRadius: BorderRadius.circular(16),
              child: Image.network(
                'https://raw.githubusercontent.com/827vzizb/Bsksnwbs/60e965684de120fbf51128c0ecdd543cf37c02b7/Screenshot_20261030_115706_Google.jpg',
                height: 130,
                width: double.infinity,
                fit: BoxFit.cover,
              ),
            ),
            const SizedBox(height: 16),
            // Professional Full Screen Flight Arena
            Container(
              height: 240,
              width: double.infinity,
              decoration: BoxDecoration(
                color: const Color(0xFF161622),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.redAccent.withOpacity(0.5)),
              ),
              child: Stack(
                alignment: Alignment.center,
                children: [
                  Positioned(
                    top: 20,
                    child: Text(
                      hasCrashed ? 'CRASHED @ ${multiplier.toStringAsFixed(2)}x' : '${multiplier.toStringAsFixed(2)}x',
                      style: TextStyle(fontSize: 34, fontWeight: FontWeight.bold, color: hasCrashed ? Colors.redAccent : const Color(0xFFFFD700)),
                    ),
                  ),
                  if (isPlaying)
                    AnimatedBuilder(
                      animation: _animController,
                      builder: (context, child) {
                        return Positioned(
                          bottom: 30 + (_animController.value * 90),
                          left: 40 + (_animController.value * 180),
                          child: const Icon(Icons.airplanemode_active, size: 60, color: Colors.greenAccent),
                        );
                      },
                    )
                  else
                    const Icon(Icons.airplanemode_active, size: 70, color: Colors.grey),
                ],
              ),
            ),
            const SizedBox(height: 16),
            BetSelectorWidget(currentBet: betAmount, onBetChanged: (amt) => setState(() => betAmount = amt)),
            const SizedBox(height: 25),
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: isPlaying ? Colors.greenAccent : const Color(0xFFFFD700), foregroundColor: Colors.black),
                onPressed: isPlaying ? cashOut : startGame,
                child: Text(isPlaying ? 'CASH OUT (${(betAmount * multiplier).toStringAsFixed(0)} PKR)' : 'BET & START FLIGHT', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ==========================================================
// GAME 2: CASINO SLOTS (HARD HOUSE EDGE)
// ==========================================================
class SlotsGame extends StatefulWidget {
  final String username;
  final double coins;
  final Function(double) onUpdate;

  const SlotsGame({super.key, required this.username, required this.coins, required this.onUpdate});

  @override
  State<SlotsGame> createState() => _SlotsGameState();
}

class _SlotsGameState extends State<SlotsGame> {
  final List<String> symbols = ['🍒', '🍋', '🔔', '💎', '7️⃣'];
  String s1 = '🍒', s2 = '🍋', s3 = '🔔';
  bool isSpinning = false;
  double betAmount = 100;

  void spin() {
    if (widget.coins < betAmount) {
      showPubgBanner(context, 'Insufficient Coins!');
      return;
    }
    widget.onUpdate(-betAmount);
    setState(() => isSpinning = true);

    Timer.periodic(const Duration(milliseconds: 90), (timer) {
      setState(() {
        s1 = symbols[Random().nextInt(symbols.length)];
        s2 = symbols[Random().nextInt(symbols.length)];
        s3 = symbols[Random().nextInt(symbols.length)];
      });
      if (timer.tick > 20) {
        timer.cancel();
        setState(() => isSpinning = false);
        checkWin();
      }
    });
  }

  void checkWin() {
    bool forceWin = Random().nextDouble() < 0.15;
    if (forceWin) {
      s1 = s2 = s3 = '7️⃣';
      double win = betAmount * 1.5;
      widget.onUpdate(win);
      showPubgBanner(context, 'Congratulations You win ${win.toStringAsFixed(0)} PKR Coins (1 Coins = 1 PKR)', isWin: true);
    } else {
      showPubgBanner(context, 'Slots Defeat! Better luck next time.');
    }
  }

  @override
  Widget build(BuildContext context) {
    return buildThemedScaffold(
      title: 'Casino Slots',
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(16),
              child: Image.network(
                'https://raw.githubusercontent.com/827vzizb/Bsksnwbs/refs/heads/main/Screenshot_20261030_115850_Google.jpg',
                height: 130,
                width: double.infinity,
                fit: BoxFit.cover,
              ),
            ),
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(color: const Color(0xFF161622), borderRadius: BorderRadius.circular(16), border: Border.all(color: Colors.amber)),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Text(s1, style: const TextStyle(fontSize: 55)),
                  Text(s2, style: const TextStyle(fontSize: 55)),
                  Text(s3, style: const TextStyle(fontSize: 55)),
                ],
              ),
            ),
            const SizedBox(height: 20),
            BetSelectorWidget(currentBet: betAmount, onBetChanged: (amt) => setState(() => betAmount = amt)),
            const SizedBox(height: 25),
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.amber, foregroundColor: Colors.black),
                onPressed: isSpinning ? null : spin,
                child: Text(isSpinning ? 'SPINNING...' : 'SPIN SLOTS', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ==========================================================
// GAME 3: LUCKY SPIN WHEEL (STRICT ACCURATE COLOR MATCH)
// ==========================================================
class SpinGame extends StatefulWidget {
  final String username;
  final double coins;
  final Function(double) onUpdate;

  const SpinGame({super.key, required this.username, required this.coins, required this.onUpdate});

  @override
  State<SpinGame> createState() => _SpinGameState();
}

class _SpinGameState extends State<SpinGame> {
  double betAmount = 100;
  bool isSpinning = false;
  double turnAngle = 0;
  String selectedColor = 'Red';
  final List<String> segmentColors = ['Red', 'Blue', 'Green', 'Orange', 'Purple', 'Teal'];

  void spinWheel() async {
    if (widget.coins < betAmount) {
      showPubgBanner(context, 'Insufficient Coins!');
      return;
    }
    widget.onUpdate(-betAmount);
    setState(() => isSpinning = true);

    // Hard House Edge logic: 85% chance to land on a random wrong color, 15% chance to land on user's selected color
    String targetLandedColor;
    if (Random().nextDouble() < 0.85) {
      List<String> wrongColors = segmentColors.where((c) => c != selectedColor).toList();
      targetLandedColor = wrongColors[Random().nextInt(wrongColors.length)];
    } else {
      targetLandedColor = selectedColor;
    }

    int targetIndex = segmentColors.indexOf(targetLandedColor);
    double targetSegmentAngle = (targetIndex * (2 * pi / 6)) + (pi / 6);
    double randomExtraSpins = (5 + Random().nextInt(5)) * 2 * pi;
    double finalRadians = randomExtraSpins + (2 * pi - targetSegmentAngle);

    setState(() {
      turnAngle += finalRadians / (2 * pi);
    });

    await Future.delayed(const Duration(seconds: 3));

    if (!mounted) return;

    if (targetLandedColor == selectedColor) {
      double win = betAmount * 1.5;
      widget.onUpdate(win);
      showPubgBanner(context, 'Congratulations You win ${win.toStringAsFixed(0)} PKR Coins (1 Coins = 1 PKR)', isWin: true);
    } else {
      showPubgBanner(context, 'Stopped on $targetLandedColor! You Lost.');
    }

    setState(() => isSpinning = false);
  }

  @override
  Widget build(BuildContext context) {
    return buildThemedScaffold(
      title: 'Lucky Casino Wheel',
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(16),
              child: Image.network(
                'https://raw.githubusercontent.com/827vzizb/Bsksnwbs/refs/heads/main/IMG-20261030-WA7462.jpg',
                height: 120,
                width: double.infinity,
                fit: BoxFit.cover,
              ),
            ),
            const SizedBox(height: 10),
            Stack(
              alignment: Alignment.topCenter,
              children: [
                AnimatedRotation(
                  turns: turnAngle,
                  duration: const Duration(seconds: 3),
                  curve: Curves.decelerate,
                  child: Container(
                    width: 210,
                    height: 210,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(color: const Color(0xFFFFD700), width: 5),
                    ),
                    child: CustomPaint(painter: RealWheelPainter()),
                  ),
                ),
                const Positioned(top: -5, child: Icon(Icons.arrow_drop_down, size: 50, color: Colors.amber)),
              ],
            ),
            const SizedBox(height: 12),
            const Text('Pick Color to Match Spin Stop:', style: TextStyle(color: Colors.grey, fontWeight: FontWeight.bold)),
            const SizedBox(height: 6),
            Wrap(
              spacing: 8,
              children: segmentColors.map((col) {
                return ChoiceChip(
                  label: Text(col),
                  selected: selectedColor == col,
                  selectedColor: Colors.amber,
                  onSelected: (val) => setState(() => selectedColor = col),
                );
              }).toList(),
            ),
            const SizedBox(height: 12),
            BetSelectorWidget(currentBet: betAmount, onBetChanged: (amt) => setState(() => betAmount = amt)),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.purpleAccent, foregroundColor: Colors.white),
                onPressed: isSpinning ? null : spinWheel,
                child: Text(isSpinning ? 'SPINNING...' : 'SPIN WHEEL', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class RealWheelPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final double radius = size.width / 2;
    final Offset center = Offset(radius, radius);
    final List<Color> colors = [Colors.red, Colors.blue, Colors.green, Colors.orange, Colors.purple, Colors.teal];
    final Paint paint = Paint()..style = PaintingStyle.fill;
    const double sweepAngle = (2 * pi) / 6;

    for (int i = 0; i < 6; i++) {
      paint.color = colors[i];
      canvas.drawArc(Rect.fromCircle(center: center, radius: radius), i * sweepAngle, sweepAngle, true, paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

// ==========================================================
// GAME 4: HIGH LOW DICE (HARD HOUSE EDGE)
// ==========================================================
class DiceGame extends StatefulWidget {
  final String username;
  final double coins;
  final Function(double) onUpdate;

  const DiceGame({super.key, required this.username, required this.coins, required this.onUpdate});

  @override
  State<DiceGame> createState() => _DiceGameState();
}

class _DiceGameState extends State<DiceGame> {
  int d1 = 1, d2 = 1;
  double betAmount = 100;
  bool guessHigh = true;

  void roll() {
    if (widget.coins < betAmount) {
      showPubgBanner(context, 'Insufficient Coins!');
      return;
    }
    widget.onUpdate(-betAmount);

    setState(() {
      d1 = Random().nextInt(6) + 1;
      d2 = Random().nextInt(6) + 1;
    });

    int sum = d1 + d2;
    bool isHigh = sum >= 7;

    bool forceLoss = Random().nextDouble() < 0.8;
    if (forceLoss) {
      isHigh = !guessHigh;
    }

    if (guessHigh == isHigh) {
      double win = betAmount * 1.5;
      widget.onUpdate(win);
      showPubgBanner(context, 'Congratulations You win ${win.toStringAsFixed(0)} PKR Coins (1 Coins = 1 PKR)', isWin: true);
    } else {
      showPubgBanner(context, 'Dice Roll Defeat! Sum was $sum.');
    }
  }

  @override
  Widget build(BuildContext context) {
    return buildThemedScaffold(
      title: 'Dice High/Low',
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(16),
              child: Image.network(
                'https://raw.githubusercontent.com/827vzizb/Bsksnwbs/refs/heads/main/IMG-20261030-WA9934.jpg',
                height: 130,
                width: double.infinity,
                fit: BoxFit.cover,
              ),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text('$d1', style: const TextStyle(fontSize: 70, fontWeight: FontWeight.bold, color: Colors.blueAccent)),
                const SizedBox(width: 20),
                Text('$d2', style: const TextStyle(fontSize: 70, fontWeight: FontWeight.bold, color: Colors.blueAccent)),
              ],
            ),
            const SizedBox(height: 10),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ChoiceChip(label: const Text('High (7-12)'), selected: guessHigh, onSelected: (v) => setState(() => guessHigh = true)),
                const SizedBox(width: 10),
                ChoiceChip(label: const Text('Low (2-6)'), selected: !guessHigh, onSelected: (v) => setState(() => guessHigh = false)),
              ],
            ),
            const SizedBox(height: 20),
            BetSelectorWidget(currentBet: betAmount, onBetChanged: (amt) => setState(() => betAmount = amt)),
            const SizedBox(height: 25),
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.blueAccent, foregroundColor: Colors.white),
                onPressed: roll,
                child: const Text('ROLL DICE', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ==========================================================
// GAME 5: MINESWEEPER HARD
// ==========================================================
class MinesGame extends StatefulWidget {
  final String username;
  final double coins;
  final Function(double) onUpdate;

  const MinesGame({super.key, required this.username, required this.coins, required this.onUpdate});

  @override
  State<MinesGame> createState() => _MinesGameState();
}

class _MinesGameState extends State<MinesGame> {
  List<bool> revealed = List.filled(9, false);
  List<bool> mines = List.filled(9, false);
  bool inProgress = false;
  double betAmount = 100;

  void startGame() {
    if (widget.coins < betAmount) {
      showPubgBanner(context, 'Insufficient Coins!');
      return;
    }
    widget.onUpdate(-betAmount);
    setState(() {
      revealed = List.filled(9, false);
      mines = List.filled(9, false);
      int placed = 0;
      while (placed < 6) {
        int idx = Random().nextInt(9);
        if (!mines[idx]) {
          mines[idx] = true;
          placed++;
        }
      }
      inProgress = true;
    });
  }

  void tapTile(int idx) {
    if (!inProgress || revealed[idx]) return;
    setState(() => revealed[idx] = true);

    if (mines[idx]) {
      setState(() => inProgress = false);
      showPubgBanner(context, 'BOOM! Mine Exploded. You Lost.');
    } else {
      double win = betAmount * 1.5;
      widget.onUpdate(win);
      setState(() => inProgress = false);
      showPubgBanner(context, 'Congratulations You win ${win.toStringAsFixed(0)} PKR Coins (1 Coins = 1 PKR)', isWin: true);
    }
  }

  @override
  Widget build(BuildContext context) {
    return buildThemedScaffold(
      title: 'Minesweeper Hard',
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(16),
              child: Image.network(
                'https://raw.githubusercontent.com/827vzizb/Bsksnwbs/refs/heads/main/IMG-20261030-WA3036.jpg',
                height: 120,
                width: double.infinity,
                fit: BoxFit.cover,
              ),
            ),
            const SizedBox(height: 16),
            GridView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3, crossAxisSpacing: 8, mainAxisSpacing: 8),
              itemCount: 9,
              itemBuilder: (context, idx) => GestureDetector(
                onTap: () => tapTile(idx),
                child: Container(
                  decoration: BoxDecoration(
                    color: revealed[idx] ? (mines[idx] ? Colors.red : Colors.green) : const Color(0xFF161622),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Center(child: Text(revealed[idx] ? (mines[idx] ? '💥' : '💎') : '?', style: const TextStyle(fontSize: 28))),
                ),
              ),
            ),
            const SizedBox(height: 16),
            BetSelectorWidget(currentBet: betAmount, onBetChanged: (amt) => setState(() => betAmount = amt)),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.greenAccent, foregroundColor: Colors.black),
                onPressed: inProgress ? null : startGame,
                child: Text(inProgress ? 'TAP TILES' : 'START MINES', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ==========================================================
// GAME 6: LIMBO ROCKET (PROFESSIONAL FULL SCREEN ANIMATION)
// ==========================================================
class LimboGame extends StatefulWidget {
  final String username;
  final double coins;
  final Function(double) onUpdate;

  const LimboGame({super.key, required this.username, required this.coins, required this.onUpdate});

  @override
  State<LimboGame> createState() => _LimboGameState();
}

class _LimboGameState extends State<LimboGame> with SingleTickerProviderStateMixin {
  double targetMult = 2.0;
  double betAmount = 100;
  bool isLaunching = false;
  late AnimationController _rocketController;

  @override
  void initState() {
    super.initState();
    _rocketController = AnimationController(vsync: this, duration: const Duration(seconds: 1));
  }

  @override
  void dispose() {
    _rocketController.dispose();
    super.dispose();
  }

  void play() async {
    if (widget.coins < betAmount) {
      showPubgBanner(context, 'Insufficient Coins!');
      return;
    }
    widget.onUpdate(-betAmount);
    setState(() => isLaunching = true);
    _rocketController.repeat(reverse: true);

    await Future.delayed(const Duration(seconds: 2));
    _rocketController.stop();

    double rolled = 1.0 + (Random().nextDouble() * 2.0);

    if (!mounted) return;

    if (rolled >= targetMult) {
      double win = betAmount * targetMult;
      widget.onUpdate(win);
      showPubgBanner(context, 'Congratulations You win ${win.toStringAsFixed(0)} PKR Coins (1 Coins = 1 PKR)', isWin: true);
    } else {
      showPubgBanner(context, 'Rolled ${rolled.toStringAsFixed(2)}x - Defeat!');
    }
    setState(() => isLaunching = false);
  }

  @override
  Widget build(BuildContext context) {
    return buildThemedScaffold(
      title: 'Limbo Rocket',
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(16),
              child: Image.network(
                'https://raw.githubusercontent.com/827vzizb/Bsksnwbs/refs/heads/main/IMG-20261030-WA8013.jpg',
                height: 120,
                width: double.infinity,
                fit: BoxFit.cover,
              ),
            ),
            const SizedBox(height: 16),
            Container(
              height: 200,
              width: double.infinity,
              decoration: BoxDecoration(
                color: const Color(0xFF161622),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.orangeAccent.withOpacity(0.5)),
              ),
              child: Stack(
                alignment: Alignment.center,
                children: [
                  Positioned(
                    top: 15,
                    child: Text('Target: ${targetMult.toStringAsFixed(1)}x', style: const TextStyle(fontSize: 26, fontWeight: FontWeight.bold, color: Colors.orangeAccent)),
                  ),
                  AnimatedBuilder(
                    animation: _rocketController,
                    builder: (context, child) {
                      return Positioned(
                        bottom: isLaunching ? 20 + (_rocketController.value * 100) : 30,
                        child: const Icon(Icons.rocket_launch, size: 65, color: Colors.orangeAccent),
                      );
                    },
                  ),
                ],
              ),
            ),
            const SizedBox(height: 10),
            Slider(
              value: targetMult,
              min: 1.2,
              max: 5.0,
              divisions: 38,
              onChanged: (v) => setState(() => targetMult = v),
            ),
            const SizedBox(height: 10),
            BetSelectorWidget(currentBet: betAmount, onBetChanged: (amt) => setState(() => betAmount = amt)),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.orangeAccent, foregroundColor: Colors.black),
                onPressed: isLaunching ? null : play,
                child: Text(isLaunching ? 'LAUNCHING ROCKET...' : 'PLAY LIMBO', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
