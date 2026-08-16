// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:nurux_app/main.dart';

void main() {
  testWidgets('NuruX app renders its splash screen', (WidgetTester tester) async {
    await tester.pumpWidget(const NuruxApp());

    expect(find.text('NuruX'), findsOneWidget);
    expect(find.text('Next generation intelligent workforce'), findsOneWidget);

    await tester.pumpWidget(const SizedBox.shrink());
    await tester.pump(const Duration(seconds: 2));
  });
}
