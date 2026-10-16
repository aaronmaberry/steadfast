import { useEffect, useState } from 'react';
import { Linking, Platform, Pressable, StyleSheet, Text, View } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import content from '@steadfast/content';
import PlumbMark from './components/PlumbMark';
import HomeScreen from './screens/HomeScreen';
import TrainingScreen from './screens/TrainingScreen';
import StoreScreen from './screens/StoreScreen';
import DailyScreen from './screens/DailyScreen';
import { canOpenExternalUrl, loadPurchaseGate } from './lib/purchasePolicy';

const NAVY = '#0B1F38';
const GOLD = '#E3C572';
const BONE = '#E6DDCC';

const TABS = (content.mobile && content.mobile.tabs) || [
  { key: 'home', label: 'Home' },
  { key: 'daily', label: 'Daily' },
  { key: 'training', label: 'Training' },
  { key: 'store', label: 'Store' },
];

function openAllowedLink(url) {
  if (!canOpenExternalUrl(url)) return;
  Linking.openURL(url);
}

export default function App() {
  const [tab, setTab] = useState('home');
  const [purchasesAllowed, setPurchasesAllowed] = useState(false);
  const brand = content.brand || {};
  const url = content.SITE_URL || brand.siteUrl || 'https://walksteadfast.com';
  const openLabel = (content.mobile && content.mobile.openStore) || 'Open the store';

  useEffect(() => {
    let active = true;
    loadPurchaseGate({ platform: Platform.OS }).then((gate) => {
      if (active) setPurchasesAllowed(gate.purchasesAllowed === true);
    });
    return () => {
      active = false;
    };
  }, []);

  return (
    <View style={styles.root}>
      <StatusBar style="light" />
      <View style={styles.header}>
        <PlumbMark color={BONE} height={40} />
        <Text style={styles.headerBrand}>{brand.lockup || 'STEADFAST MEN'}</Text>
      </View>
      <View style={styles.body}>
        {tab === 'home' ? <HomeScreen /> : null}
        {tab === 'daily' ? <DailyScreen /> : null}
        {tab === 'training' ? <TrainingScreen /> : null}
        {tab === 'store' ? <StoreScreen /> : null}
      </View>
      <View style={styles.chrome}>
        {purchasesAllowed ? (
          <Pressable
            onPress={() => openAllowedLink(url)}
            style={styles.goldBtn}
            accessibilityRole="button"
            accessibilityLabel={openLabel}
          >
            <Text style={styles.goldText}>{openLabel}</Text>
          </Pressable>
        ) : null}
        <View style={styles.tabs}>
          {TABS.map((item) => {
            const active = item.key === tab;
            return (
              <Pressable
                key={item.key}
                onPress={() => setTab(item.key)}
                style={styles.tab}
                accessibilityRole="button"
              >
                <Text style={styles.tabText}>{item.label}</Text>
                {active ? <View style={styles.tabRule} /> : <View style={styles.tabRuleOff} />}
              </Pressable>
            );
          })}
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: NAVY },
  header: {
    backgroundColor: NAVY,
    paddingTop: 48,
    paddingBottom: 10,
    alignItems: 'center',
  },
  headerBrand: {
    color: BONE,
    fontSize: 11,
    letterSpacing: 2,
    fontWeight: '500',
    marginTop: 4,
  },
  body: { flex: 1, backgroundColor: BONE },
  chrome: { backgroundColor: NAVY, paddingHorizontal: 20, paddingBottom: 18, paddingTop: 12 },
  goldBtn: {
    backgroundColor: GOLD,
    minHeight: 44,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 10,
  },
  goldText: { color: NAVY, fontSize: 16, fontWeight: '500' },
  tabs: { flexDirection: 'row' },
  tab: { flex: 1, minHeight: 44, alignItems: 'center', justifyContent: 'center' },
  tabText: { color: BONE, fontSize: 13, fontWeight: '500' },
  tabRule: { marginTop: 6, height: 1, width: 28, backgroundColor: BONE },
  tabRuleOff: { marginTop: 6, height: 1, width: 28, backgroundColor: 'transparent' },
});
