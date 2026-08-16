import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'package:intl/intl.dart';

class LeaveScreen extends StatefulWidget {
  const LeaveScreen({super.key});

  @override
  State<LeaveScreen> createState() => _LeaveScreenState();
}

class _LeaveScreenState extends State<LeaveScreen> {
  final ApiService _apiService = ApiService();
  
  bool _isLoading = true;
  List<dynamic> _leaveBalances = [];
  List<dynamic> _leaveRequests = [];
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _fetchLeaveData();
  }

  Future<void> _fetchLeaveData() async {
    setState(() => _isLoading = true);
    try {
      final balances = await _apiService.getLeaveBalances();
      final requests = await _apiService.getLeaveRequests();
      
      if (!mounted) return;
      setState(() {
        _leaveBalances = balances;
        _leaveRequests = requests;
        _isLoading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _errorMessage = e.toString();
        _isLoading = false;
      });
    }
  }

  void _showRequestModal() {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: Colors.transparent,
      builder: (context) => const LeaveRequestModal(),
    ).then((value) {
      if (value == true) {
        _fetchLeaveData(); // refresh data after submission
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Color(0xFF0F172A)),
          onPressed: () => Navigator.pop(context),
        ),
        title: const Text('Leave Management', style: TextStyle(color: Color(0xFF0F172A), fontWeight: FontWeight.bold)),
        centerTitle: true,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: Color(0xFF10B981)))
          : _errorMessage != null
              ? Center(child: Text(_errorMessage!, style: const TextStyle(color: Colors.red)))
              : RefreshIndicator(
                  onRefresh: _fetchLeaveData,
                  child: ListView(
                    padding: const EdgeInsets.all(24.0),
                    children: [
                      const Text('Your Balances', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF0F172A))),
                      const SizedBox(height: 16),
                      if (_leaveBalances.isEmpty)
                        const Text("No leave balances allocated yet.", style: TextStyle(color: Colors.grey))
                      else
                        ..._leaveBalances.map((balance) => _buildBalanceCard(balance)),
                      
                      const SizedBox(height: 32),
                      const Text('Leave History', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Color(0xFF0F172A))),
                      const SizedBox(height: 16),
                      if (_leaveRequests.isEmpty)
                        const Text("No leave requests found.", style: TextStyle(color: Colors.grey))
                      else
                        ..._leaveRequests.map((request) => _buildRequestItem(request)),
                    ],
                  ),
                ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _showRequestModal,
        backgroundColor: const Color(0xFF0F172A),
        icon: const Icon(Icons.add, color: Colors.white),
        label: const Text('Request Leave', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
      ),
    );
  }

  Widget _buildBalanceCard(dynamic balance) {
    int total = balance['total_allocated'] ?? 0;
    int used = balance['used_days'] ?? 0;
    int remaining = total - used;
    String type = balance['leave_type'] ?? 'Leave';

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: const Color(0xFFF8FAFC),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(type, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF0F172A))),
              Text('$remaining days left', style: const TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF10B981))),
            ],
          ),
          const SizedBox(height: 16),
          ClipRRect(
            borderRadius: BorderRadius.circular(8),
            child: LinearProgressIndicator(
              value: total > 0 ? (used / total) : 0,
              minHeight: 10,
              backgroundColor: const Color(0xFFE2E8F0),
              color: remaining == 0 ? Colors.red : const Color(0xFF10B981),
            ),
          ),
          const SizedBox(height: 12),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('$used Used', style: const TextStyle(color: Colors.grey, fontSize: 12)),
              Text('$total Total', style: const TextStyle(color: Colors.grey, fontSize: 12)),
            ],
          )
        ],
      ),
    );
  }

  Widget _buildRequestItem(dynamic request) {
    String type = request['leave_type'] ?? 'Leave';
    String status = request['status'] ?? 'PENDING';
    String startDate = request['start_date'] ?? '';
    String endDate = request['end_date'] ?? '';
    String reason = request['reason'] ?? '';

    Color statusColor;
    Color statusBg;
    if (status.contains('APPROVED')) {
      statusColor = const Color(0xFF10B981);
      statusBg = const Color(0xFFE6F7F1);
    } else if (status == 'REJECTED') {
      statusColor = Colors.red;
      statusBg = Colors.red.shade50;
    } else {
      statusColor = const Color(0xFFD97706);
      statusBg = const Color(0xFFFEF3C7);
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: const Color(0xFFE2E8F0)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(type, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: statusBg,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  status.replaceAll('_', ' '),
                  style: TextStyle(color: statusColor, fontSize: 10, fontWeight: FontWeight.bold),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text('$startDate to $endDate', style: const TextStyle(color: Colors.grey, fontSize: 13)),
          if (reason.isNotEmpty) ...[
            const SizedBox(height: 8),
            Text(reason, style: const TextStyle(color: Color(0xFF475569), fontSize: 14)),
          ]
        ],
      ),
    );
  }
}

class LeaveRequestModal extends StatefulWidget {
  const LeaveRequestModal({super.key});

  @override
  State<LeaveRequestModal> createState() => _LeaveRequestModalState();
}

class _LeaveRequestModalState extends State<LeaveRequestModal> {
  final ApiService _apiService = ApiService();
  bool _isSubmitting = false;
  
  String _selectedType = 'ANNUAL';
  DateTime? _startDate;
  DateTime? _endDate;
  final TextEditingController _reasonController = TextEditingController();

  final List<String> _leaveTypes = ['ANNUAL', 'CASUAL', 'MEDICAL', 'COMPASSIONATE'];

  Future<void> _selectDate(BuildContext context, bool isStart) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime(2030),
    );
    if (picked != null) {
      setState(() {
        if (isStart) {
          _startDate = picked;
          if (_endDate != null && _endDate!.isBefore(_startDate!)) {
            _endDate = _startDate;
          }
        } else {
          _endDate = picked;
        }
      });
    }
  }

  Future<void> _submit() async {
    if (_startDate == null || _endDate == null || _reasonController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Please fill all fields")),
      );
      return;
    }
    
    setState(() => _isSubmitting = true);
    try {
      final DateFormat formatter = DateFormat('yyyy-MM-dd');
      await _apiService.submitLeaveRequest(
        leaveType: _selectedType,
        startDate: formatter.format(_startDate!),
        endDate: formatter.format(_endDate!),
        reason: _reasonController.text.trim(),
      );
      if (!mounted) return;
      Navigator.pop(context, true);
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error: ${e.toString()}")),
      );
    } finally {
      if (mounted) setState(() => _isSubmitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.only(
        bottom: MediaQuery.of(context).viewInsets.bottom,
        left: 24,
        right: 24,
        top: 24,
      ),
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text("Request Leave", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          
          const Text("Leave Type", style: TextStyle(fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          DropdownButtonFormField<String>(
            initialValue: _selectedType,
            decoration: InputDecoration(
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
              contentPadding: const EdgeInsets.symmetric(horizontal: 16),
            ),
            items: _leaveTypes.map((type) {
              return DropdownMenuItem(value: type, child: Text(type));
            }).toList(),
            onChanged: (val) {
              if (val != null) setState(() => _selectedType = val);
            },
          ),
          
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text("Start Date", style: TextStyle(fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    InkWell(
                      onTap: () => _selectDate(context, true),
                      child: Container(
                        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 12),
                        decoration: BoxDecoration(
                          border: Border.all(color: Colors.grey.shade300),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(_startDate != null ? DateFormat('MMM dd, yyyy').format(_startDate!) : 'Select'),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text("End Date", style: TextStyle(fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    InkWell(
                      onTap: () => _selectDate(context, false),
                      child: Container(
                        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 12),
                        decoration: BoxDecoration(
                          border: Border.all(color: Colors.grey.shade300),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(_endDate != null ? DateFormat('MMM dd, yyyy').format(_endDate!) : 'Select'),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          
          const SizedBox(height: 16),
          const Text("Reason", style: TextStyle(fontWeight: FontWeight.bold)),
          const SizedBox(height: 8),
          TextField(
            controller: _reasonController,
            maxLines: 3,
            decoration: InputDecoration(
              hintText: "Why are you requesting leave?",
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
            ),
          ),
          
          const SizedBox(height: 24),
          SizedBox(
            width: double.infinity,
            height: 50,
            child: ElevatedButton(
              onPressed: _isSubmitting ? null : _submit,
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF0F172A),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
              child: _isSubmitting
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text("Submit Request", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
            ),
          ),
          const SizedBox(height: 32),
        ],
      ),
    );
  }
}
